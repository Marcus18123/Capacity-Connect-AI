const TrainerDashboard = {
  init: async function() {
    try {
      const data = await window.api.get('/trainer/dashboard');
      this.renderTrainerInfo(data.trainer);
      this.renderExpertise(data.expertise);
      this.renderTrainees(data.assigned_trainees);
    } catch (e) {
      console.error("Failed to load trainer dashboard", e);
    }
  },

  renderTrainerInfo: function(trainer) {
    if (!trainer) return;
    const nameEl = document.getElementById('trainer-welcome');
    const statusEl = document.getElementById('trainer-approval-status');
    if (nameEl) nameEl.textContent = `Welcome, ${trainer.name}`;
    if (statusEl) {
      statusEl.textContent = trainer.approval_status;
      statusEl.className = trainer.approval_status === 'APPROVED' ? 'badge badge-success' : 'badge badge-warning';
    }
  },

  renderExpertise: function(expertiseList) {
    const container = document.getElementById('trainer-expertise-list');
    if (!container) return;

    if (!expertiseList || !expertiseList.length) {
      container.innerHTML = `<div class="text-sm text-muted">No expertise areas registered.</div>`;
      return;
    }

    let html = '';
    expertiseList.forEach(e => {
      html += `
        <div style="border: 1px solid var(--border-default); border-radius: var(--radius-sm); padding: var(--spacing-sm); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div class="font-weight-bold text-sm text-primary">${e.competency}</div>
            <div class="text-xs text-muted">Experience: ${e.years_experience} yrs</div>
          </div>
          <span class="badge badge-ai">Proficiency: ${e.proficiency_level} / 5</span>
        </div>
      `;
    });
    container.innerHTML = html;
  },

  renderTrainees: function(trainees) {
    const tbody = document.getElementById('trainer-trainees-table');
    if (!tbody) return;

    if (!trainees || !trainees.length) {
      tbody.innerHTML = `
        <tr>
          <td colspan="4" style="padding: var(--spacing-md); text-align: center;" class="text-muted">
            No trainees assigned.
          </td>
        </tr>
      `;
      return;
    }

    let html = '';
    trainees.forEach(t => {
      html += `
        <tr style="border-bottom: 1px solid var(--border-default);">
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-weight: 600; color: var(--color-primary);">${t.name}</td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">${t.email}</td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">${t.competencies_count}</td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-weight: 700; color: var(--color-success);">${t.average_proficiency} / 5.0</td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('trainer-trainees-table')) {
    TrainerDashboard.init();
  }
});
