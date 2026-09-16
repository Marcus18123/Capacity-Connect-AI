/**
 * CAPACITY CONNECT AI - Skill Gap Logic
 */

const SkillGap = {
  init: function() {
    this.renderGapComparisons();
    this.bindGenerateButton();
  },

  renderGapComparisons: function() {
    const container = document.getElementById('gap-comparison-list');
    if (!container) return;

    let html = '';
    mockData.skillGaps.forEach(gap => {
      
      let badgeClass = AppUtils.getPriorityClass(gap.priority);

      html += `
        <div class="gap-comparison">
          <div>
            <div class="font-weight-bold text-primary mb-xs">${gap.competency}</div>
            <span class="badge ${badgeClass}">${gap.priority} PRIORITY</span>
          </div>
          
          <div class="gap-bars">
            <div class="gap-bar-row">
              <span class="gap-bar-label">Current</span>
              <div class="progress-container" style="flex: 1; margin: 0; background-color: var(--color-neutral-light);">
                <div class="progress-bar" style="width: ${gap.current}%; background-color: var(--color-secondary);"></div>
              </div>
              <span class="text-xs text-primary" style="width: 25px;">${gap.current}</span>
            </div>
            
            <div class="gap-bar-row">
              <span class="gap-bar-label">Target</span>
              <div class="progress-container" style="flex: 1; margin: 0; background-color: var(--color-neutral-light);">
                <div class="progress-bar" style="width: ${gap.target}%; background-color: var(--color-tertiary);"></div>
              </div>
              <span class="text-xs text-primary" style="width: 25px;">${gap.target}</span>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  bindGenerateButton: function() {
    const btn = document.getElementById('generate-path-btn');
    const notif = document.getElementById('ai-notification');
    
    if (btn && notif) {
      btn.addEventListener('click', () => {
        notif.style.display = 'block';
        setTimeout(() => {
          window.location.href = 'learning-path.html';
        }, 1500);
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('gap-comparison-list')) {
    SkillGap.init();
  }
});
