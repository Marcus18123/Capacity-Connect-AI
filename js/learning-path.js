/**
 * CAPACITY CONNECT AI - Learning Path Logic
 */

const LearningPath = {
  init: function() {
    this.renderPathSteps();
  },

  renderPathSteps: function() {
    const container = document.getElementById('learning-path-steps');
    if (!container) return;

    // Hardcoded extended path specifically for this view to match requirements
    const steps = [
      { id: 1, title: "Statistics Fundamentals", comp: "Statistics", duration: "2 weeks", diff: "Beginner", status: "Completed", icon: "✓" },
      { id: 2, title: "Data Visualization", comp: "Data Analysis", duration: "1 week", diff: "Intermediate", status: "Completed", icon: "✓" },
      { id: 3, title: "Time-Series Analysis", comp: "Time-Series Forecasting", duration: "3 weeks", diff: "Advanced", status: "In Progress", icon: "3", progress: 45 },
      { id: 4, title: "Machine Learning Foundations", comp: "Machine Learning", duration: "4 weeks", diff: "Intermediate", status: "Upcoming", icon: "4" },
      { id: 5, title: "Applied Agentic Project", comp: "Multi-Agent Swarms", duration: "2 weeks", diff: "Advanced", status: "Locked", icon: "🔒" }
    ];

    let html = '';
    steps.forEach(step => {
      
      let stepClass = '';
      let actionBtn = '';
      let progressHtml = '';

      if (step.status === 'Completed') {
        stepClass = 'completed';
        actionBtn = `<button class="btn btn-outline" style="font-size: var(--text-xs); padding: 0.25rem 0.5rem;">Review</button>`;
      } else if (step.status === 'In Progress') {
        stepClass = 'active';
        actionBtn = `<button class="btn btn-primary" style="font-size: var(--text-xs); padding: 0.25rem 0.5rem;">Continue</button>`;
        progressHtml = `
          <div class="progress-container mt-sm" style="height: 4px; width: 100px;">
            <div class="progress-bar" style="width: ${step.progress}%"></div>
          </div>
        `;
      } else {
        actionBtn = `<span class="text-xs text-muted">${step.status}</span>`;
      }

      html += `
        <div class="path-step ${stepClass}">
          <div class="step-number">${step.icon}</div>
          <div class="step-content">
            <div class="flex justify-between items-start">
              <div>
                <h4 style="color: var(--color-primary); margin-bottom: 4px;">${step.title}</h4>
                <div class="text-xs text-muted flex gap-sm" style="flex-wrap: wrap;">
                  <span><strong class="text-neutral">Competency:</strong> ${step.comp}</span>
                  <span>|</span>
                  <span><strong class="text-neutral">Duration:</strong> ${step.duration}</span>
                  <span>|</span>
                  <span><strong class="text-neutral">Difficulty:</strong> ${step.diff}</span>
                </div>
                ${progressHtml}
              </div>
              <div>
                ${actionBtn}
              </div>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('learning-path-steps')) {
    LearningPath.init();
  }
});
