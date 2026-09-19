const SkillGap = {
  data: null,

  init: async function() {
    try {
      this.data = await window.api.get('/trainees/me/skill-gaps');
      this.renderGapComparisons();
      this.bindGenerateButton();
      this.updateAlignment();
    } catch (error) {
      console.error('Failed to load skill gaps:', error);
      const container = document.getElementById('gap-comparison-list');
      if (container) {
        container.innerHTML = `
          <div style="padding: var(--spacing-md); text-align: center;">
            Failed to load skill gap data.
          </div>
        `;
      }
    }
  },

  getPriority: function(gap) {
    if (gap <= 0) return 'MET';
    if (gap >= 1.5) return 'HIGH';
    if (gap >= 1) return 'MEDIUM';
    return 'LOW';
  },

  getPriorityClass: function(priority) {
    if (priority === 'HIGH') return 'badge-danger';
    if (priority === 'MEDIUM') return 'badge-warning';
    if (priority === 'LOW') return 'badge-ai';
    return 'badge-success';
  },

  renderGapComparisons: function() {
    const container = document.getElementById('gap-comparison-list');
    if (!container || !this.data) return;

    let html = '';

    this.data.skill_gaps.forEach(gap => {
      const priority = this.getPriority(gap.gap);
      const badgeClass = this.getPriorityClass(priority);

      const currentPercent = Math.min(
        100,
        Math.max(0, (gap.current_level / 5) * 100)
      );

      const targetPercent = Math.min(
        100,
        Math.max(0, (gap.required_level / 5) * 100)
      );

      html += `
        <div class="gap-comparison">
          <div>
            <div class="font-weight-bold text-primary mb-xs">${gap.competency}</div>
            <span class="badge ${badgeClass}">${priority} PRIORITY</span>
          </div>

          <div class="gap-bars">
            <div class="gap-bar-row">
              <span class="gap-bar-label">Current</span>
              <div class="progress-container" style="flex: 1; margin: 0; background-color: var(--color-neutral-light);">
                <div class="progress-bar" style="width: ${currentPercent}%; background-color: var(--color-secondary);"></div>
              </div>
              <span class="text-xs text-primary" style="width: 45px;">${gap.current_level}</span>
            </div>

            <div class="gap-bar-row">
              <span class="gap-bar-label">Target</span>
              <div class="progress-container" style="flex: 1; margin: 0; background-color: var(--color-neutral-light);">
                <div class="progress-bar" style="width: ${targetPercent}%; background-color: var(--color-tertiary);"></div>
              </div>
              <span class="text-xs text-primary" style="width: 45px;">${gap.required_level}</span>
            </div>
          </div>
        </div>
      `;
    });

    if (!this.data.skill_gaps.length) {
      html = `
        <div style="padding: var(--spacing-md); text-align: center;">
          No skill requirements found.
        </div>
      `;
    }

    container.innerHTML = html;
  },

  updateAlignment: function() {
    const alignmentElements = document.querySelectorAll('[data-skill-alignment]');

    alignmentElements.forEach(element => {
      element.textContent = `${this.data.overall_alignment}%`;
    });

    const roleElements = document.querySelectorAll('[data-target-role]');

    roleElements.forEach(element => {
      element.textContent = this.data.target_role;
    });
  },

  bindGenerateButton: function() {
    const btn = document.getElementById('generate-path-btn');
    const notif = document.getElementById('ai-notification');

    if (btn) {
      btn.addEventListener('click', async () => {
        if (notif) {
          notif.textContent = "AI engine generating custom learning path...";
          notif.style.display = 'block';
        }

        try {
          await window.api.post('/ai/generate-learning-path', {
            target_role: this.data?.target_role || "Data Analyst"
          });
          setTimeout(() => {
            window.location.href = 'learning-path.html';
          }, 800);
        } catch (e) {
          console.error("AI Learning Path generation error", e);
          window.location.href = 'learning-path.html';
        }
      });
    }
  }

};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('gap-comparison-list')) {
    SkillGap.init();
  }
});