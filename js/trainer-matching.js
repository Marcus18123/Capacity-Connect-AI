const TrainerMatching = {
  data: [],

  init: async function() {
    try {
      this.data = await window.api.get('/trainees/me/recommended-trainers');
      this.renderTrainers();
    } catch (error) {
      console.error('Failed to load recommended trainers:', error);

      const container = document.getElementById('trainer-cards-container');

      if (container) {
        container.innerHTML = `
          <div style="padding: var(--spacing-md); text-align: center;">
            Failed to load recommended trainers.
          </div>
        `;
      }
    }
  },

  renderTrainers: function() {
    const container = document.getElementById('trainer-cards-container');

    if (!container) return;

    if (!this.data.length) {
      container.innerHTML = `
        <div style="padding: var(--spacing-md); text-align: center;">
          No recommended trainers found.
        </div>
      `;
      return;
    }

    let html = '';

    this.data.forEach(trainer => {
      const initials = trainer.name
        .replace(/[^a-zA-Z ]/g, '')
        .split(' ')
        .map(name => name[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();

      const matchedCompetencies = trainer.matchedCompetencies?.length
        ? trainer.matchedCompetencies.join(', ')
        : 'No direct competency match';

      html += `
        <div class="card" style="display: flex; gap: var(--spacing-xl); flex-wrap: wrap;">

          <div style="flex: 1; min-width: 250px; display: flex; gap: var(--spacing-md); align-items: flex-start;">
            <div style="width: 64px; height: 64px; border-radius: 50%; background-color: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center; font-size: var(--text-xl); font-weight: 700; flex-shrink: 0;">
              ${initials}
            </div>

            <div>
              <h3 style="font-size: var(--text-lg); color: var(--color-primary); margin-bottom: 4px;">
                ${trainer.name}
              </h3>

              <div class="text-sm text-muted mb-xs">
                <strong class="text-neutral">Experience:</strong>
                ${trainer.experience}
              </div>

              <div class="text-sm text-muted mb-sm">
                <strong class="text-neutral">Availability:</strong>
                <span class="text-success">${trainer.availability}</span>
              </div>

              <button class="btn btn-primary" style="padding: 0.25rem 0.75rem; font-size: var(--text-xs);">
                Connect
              </button>
            </div>
          </div>

          <div style="flex: 1.5; min-width: 300px; border-left: 1px solid var(--border-default); padding-left: var(--spacing-lg);">

            <div class="flex justify-between items-start mb-sm">
              <span class="badge badge-ai">
                Expertise Match: ${trainer.matchScore}%
              </span>
            </div>

            <p class="text-sm text-muted mb-md">
              <strong class="text-neutral">Competencies Covered:</strong><br>
              ${trainer.expertise}
            </p>

            <div style="background-color: var(--bg-canvas); padding: var(--spacing-sm); border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
              <div class="text-xs font-weight-bold text-secondary mb-xs">
                Why this trainer matches:
              </div>

              <p class="text-xs text-muted" style="margin: 0;">
                ${trainer.reason}
              </p>

              <p class="text-xs text-muted" style="margin: 6px 0 0;">
                <strong class="text-neutral">Matched skill gap:</strong>
                ${matchedCompetencies}
              </p>
            </div>

          </div>

        </div>
      `;
    });

    container.innerHTML = html;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('trainer-cards-container')) {
    TrainerMatching.init();
  }
});