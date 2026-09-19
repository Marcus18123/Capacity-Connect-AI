const LearningPath = {
  data: null,

  init: async function() {
    try {
      this.data = await window.api.get('/trainees/me/learning-path');
      this.renderPathSteps();
      this.updatePathInfo();
    } catch (error) {
      console.error('Failed to load learning path:', error);

      const container = document.getElementById('learning-path-steps');

      if (container) {
        container.innerHTML = `
          <div style="padding: var(--spacing-md); text-align: center;">
            Failed to load learning path.
          </div>
        `;
      }
    }
  },

  formatStatus: function(status) {
    return status
      .toLowerCase()
      .replace(/_/g, ' ')
      .replace(/\b\w/g, char => char.toUpperCase());
  },

  renderPathSteps: function() {
    const container = document.getElementById('learning-path-steps');

    if (!container || !this.data) return;

    let html = '';

    this.data.items.forEach(step => {
      const status = this.formatStatus(step.status);

      let stepClass = '';
      let actionBtn = '';
      let progressHtml = '';

      if (step.status === 'COMPLETED') {
        stepClass = 'completed';
        actionBtn = `
          <button class="btn btn-outline" style="font-size: var(--text-xs); padding: 0.25rem 0.5rem;" disabled>
            Completed ✓
          </button>
        `;
      } else if (step.status === 'IN_PROGRESS') {
        stepClass = 'active';
        actionBtn = `
          <button class="btn btn-primary" style="font-size: var(--text-xs); padding: 0.25rem 0.5rem;" onclick="LearningPath.updateStepStatus('${step.id}', 'COMPLETED')">
            Mark Complete
          </button>
        `;
        progressHtml = `
          <div class="progress-container mt-sm" style="height: 4px; width: 100px;">
            <div class="progress-bar" style="width: ${step.progress_percentage || 50}%"></div>
          </div>
        `;
      } else if (step.status === 'AVAILABLE') {
        actionBtn = `
          <button class="btn btn-primary" style="font-size: var(--text-xs); padding: 0.25rem 0.5rem;" onclick="LearningPath.updateStepStatus('${step.id}', 'IN_PROGRESS')">
            Start Step
          </button>
        `;
      } else {
        actionBtn = `
          <span class="text-xs text-muted">Locked</span>
        `;
      }


      const icon = step.status === 'COMPLETED'
        ? '✓'
        : step.sequence;

      html += `
        <div class="path-step ${stepClass}">
          <div class="step-number">${icon}</div>

          <div class="step-content">
            <div class="flex justify-between items-start">
              <div>
                <h4 style="color: var(--color-primary); margin-bottom: 4px;">
                  ${step.competency}
                </h4>

                <div class="text-xs text-muted flex gap-sm" style="flex-wrap: wrap;">
                  <span>
                    <strong class="text-neutral">Competency:</strong>
                    ${step.competency}
                  </span>

                  <span>|</span>

                  <span>
                    <strong class="text-neutral">Priority:</strong>
                    ${step.priority}
                  </span>

                  <span>|</span>

                  <span>
                    <strong class="text-neutral">Status:</strong>
                    ${status}
                  </span>
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

    if (!this.data.items.length) {
      html = `
        <div style="padding: var(--spacing-md); text-align: center;">
          No learning items are currently required.
        </div>
      `;
    }

    container.innerHTML = html;
  },

  updatePathInfo: function() {
    const alignmentElements = document.querySelectorAll('[data-learning-alignment]');

    alignmentElements.forEach(element => {
      element.textContent = `${this.data.current_alignment}%`;
    });

    const roleElements = document.querySelectorAll('[data-learning-role]');

    roleElements.forEach(element => {
      element.textContent = this.data.target_role;
    });
  },

  updateStepStatus: async function(itemId, newStatus) {
    try {
      await window.api.put(`/trainees/me/learning-path/items/${itemId}/status`, {
        status: newStatus
      });
      await this.init();
    } catch (e) {
      console.error("Failed to update step status", e);
      alert("Failed to update step: " + e.message);
    }
  }
};


document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('learning-path-steps')) {
    LearningPath.init();
  }
});