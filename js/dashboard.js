/**
 * CAPACITY CONNECT AI - Dashboard Logic
 */

const Dashboard = {
  data: null,

  init: async function() {
    try {
      if (window.api) {
        this.data = await window.api.get('/trainees/me/dashboard');
      } else {
        throw new Error("API not loaded");
      }
    } catch (e) {
      console.warn("API failed, falling back to mockData", e);
      this.data = mockData;
    }
    
    this.populateKPIs();
    this.renderCompetencyOverview();
    this.renderLearningPath();
    this.renderSkillGaps();
    this.renderRecentActivity();
    this.fetchAndRenderAIInsights();
  },

  fetchAndRenderAIInsights: async function() {
    try {
        if (window.api) {
            const insights = await window.api.get('/ai/insights');
            const container = document.getElementById('ai-insights-container');
            if (!container) {
                // If container doesn't exist, we inject it at the top of the dashboard main content
                const mainContent = document.querySelector('.main-content');
                if (mainContent) {
                    const insightHTML = insights.map(i => `
                        <div style="background: var(--bg-surface); padding: var(--spacing-md); border-radius: var(--radius-md); border-left: 4px solid var(--color-primary); margin-bottom: var(--spacing-md); box-shadow: var(--shadow-sm);">
                            <div class="flex items-center justify-between" style="margin-bottom: var(--spacing-xs);">
                                <h3 class="text-md font-weight-bold" style="margin:0;"><span style="color:var(--color-primary)">✨ AI Insight:</span> ${i.title}</h3>
                                <span class="badge ${i.severity === 'CRITICAL' ? 'danger' : 'primary'}">${i.severity}</span>
                            </div>
                            <p class="text-sm text-secondary" style="margin:0;">${i.summary}</p>
                        </div>
                    `).join('');
                    
                    const insightDiv = document.createElement('div');
                    insightDiv.innerHTML = insightHTML;
                    mainContent.insertBefore(insightDiv, mainContent.firstChild);
                }
            }
        }
    } catch(e) {
        console.warn("Could not fetch AI insights", e);
    }
  },

  populateKPIs: function() {
  const user = this.data.user || {};
  const kpis = this.data.kpis || {};

  const welcomeEl = document.getElementById('welcome-message');
  if (welcomeEl && user.name) {
    const firstName = user.name.split(' ')[0];
    welcomeEl.textContent = `Good morning, ${firstName}`;
  }

  const kpiIndex = document.getElementById('kpi-index');
  if (kpiIndex) {
    kpiIndex.textContent = `${kpis.competency_index ?? 0}%`;
  }

  const kpiLearning = document.getElementById('kpi-learning');
  if (kpiLearning) {
    kpiLearning.textContent = `${kpis.active_courses ?? 0}`;
  }

  const kpiLearningProgress = document.getElementById('kpi-learning-progress');
  if (kpiLearningProgress) {
    const progress = kpis.learning_progress ?? 0;
    kpiLearningProgress.style.width = `${Math.min(Math.max(progress, 0), 100)}%`;
  }

  const kpiGaps = document.getElementById('kpi-gaps');
  if (kpiGaps) {
    kpiGaps.textContent = kpis.skill_gap_count ?? 0;
  }

  const kpiVerified = document.getElementById('kpi-verified');
  if (kpiVerified) {
    kpiVerified.textContent = kpis.verified_competencies ?? 0;
  }
},

  renderCompetencyOverview: function() {
    const container = document.getElementById('competency-bars-container');
    if (!container) return;

    const displayComps = (this.data.competencies || mockData.competencies).slice(0, 5);

    let html = '';
    displayComps.forEach(comp => {
      html += `
        <div class="competency-item">
          <div class="competency-header">
            <span>${comp.name}</span>
            <span class="text-primary">${comp.progress}%</span>
          </div>
          <div class="progress-container">
            <div class="progress-bar ${comp.progress >= 80 ? 'success' : ''}" style="width: ${comp.progress}%"></div>
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  },

  renderLearningPath: function() {
    const path = this.data.learningPath || mockData.learningPath;
    
    const trackEl = document.getElementById('learning-path-track');
    if (trackEl) trackEl.textContent = path.track;

    const badgeEl = document.getElementById('learning-path-progress-badge');
    if (badgeEl) badgeEl.textContent = `${path.progress}% Complete`;

    const timeline = document.getElementById('learning-path-timeline');
    if (!timeline) return;

    let html = '';
    path.steps.forEach((step, index) => {
      let statusClass = '';
      if (step.status === 'Completed') statusClass = 'completed';
      if (step.status === 'In Progress') statusClass = 'active';

      html += `
        <div class="timeline-item ${statusClass}">
          <div class="text-sm font-weight-bold" style="color: ${statusClass === 'active' ? 'var(--color-primary)' : 'var(--color-neutral)'};">${step.title}</div>
          <div class="text-xs text-muted">${step.status} • ${step.type}</div>
        </div>
      `;
    });

    timeline.innerHTML = html;
  },

  renderSkillGaps: function() {
    const container = document.getElementById('skill-gap-list');
    if (!container) return;

    let html = '';
    const gaps = this.data.skillGaps || mockData.skillGaps;
    gaps.forEach(gap => {
      const badgeClass = AppUtils.getPriorityClass(gap.priority);
      html += `
        <div style="border: 1px solid var(--border-default); border-radius: var(--radius-sm); padding: var(--spacing-sm); display: flex; flex-direction: column; gap: var(--spacing-xs);">
          <div class="flex justify-between items-center">
            <span class="badge ${badgeClass}">${gap.priority}</span>
            <span class="text-xs text-muted">Target: ${gap.targetDate}</span>
          </div>
          <div class="font-weight-bold text-sm text-primary">${gap.competency}</div>
          <div class="text-xs text-secondary font-weight-bold">${gap.impact}</div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  renderRecentActivity: function() {
    const container = document.getElementById('recent-activity-list');
    if (!container) return;

    let html = '';
    const activities = this.data.recentActivity || mockData.recentActivity;
    activities.forEach(activity => {
      let icon = '📝';
      if (activity.type === 'course') icon = '📚';
      if (activity.type === 'verification') icon = '🏅';

      html += `
        <div class="flex items-center gap-sm" style="padding-bottom: var(--spacing-xs); border-bottom: 1px solid var(--border-default);">
          <div style="font-size: 1.25rem;">${icon}</div>
          <div style="flex: 1;">
            <div class="text-xs text-muted">${activity.title}</div>
            <div class="text-sm font-weight-bold text-primary">${activity.detail}</div>
          </div>
          ${activity.score ? `<div class="text-sm font-weight-bold text-success">${activity.score}</div>` : ''}
        </div>
      `;
    });

    container.innerHTML = html;
  }
};

// Initialize Dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('welcome-message')) {
    Dashboard.init();
  }
});
