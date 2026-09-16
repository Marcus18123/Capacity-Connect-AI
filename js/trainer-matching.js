/**
 * CAPACITY CONNECT AI - Trainer Matching Logic
 */

const TrainerMatching = {
  init: function() {
    this.renderTrainers();
  },

  renderTrainers: function() {
    const container = document.getElementById('trainer-cards-container');
    if (!container) return;

    let html = '';
    mockData.trainers.forEach(trainer => {
      
      const initials = trainer.name.replace(/[^a-zA-Z ]/g, "").split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

      html += `
        <div class="card" style="display: flex; gap: var(--spacing-xl); flex-wrap: wrap;">
          
          <!-- Avatar & Basics -->
          <div style="flex: 1; min-width: 250px; display: flex; gap: var(--spacing-md); align-items: flex-start;">
            <div style="width: 64px; height: 64px; border-radius: 50%; background-color: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center; font-size: var(--text-xl); font-weight: 700; flex-shrink: 0;">
              ${initials}
            </div>
            <div>
              <h3 style="font-size: var(--text-lg); color: var(--color-primary); margin-bottom: 4px;">${trainer.name}</h3>
              <div class="text-sm text-muted mb-xs"><strong class="text-neutral">Experience:</strong> ${trainer.experience}</div>
              <div class="text-sm text-muted mb-sm"><strong class="text-neutral">Availability:</strong> <span class="text-success">${trainer.availability}</span></div>
              <button class="btn btn-primary" style="padding: 0.25rem 0.75rem; font-size: var(--text-xs);">Connect</button>
            </div>
          </div>

          <!-- Expertise -->
          <div style="flex: 1.5; min-width: 300px; border-left: 1px solid var(--border-default); padding-left: var(--spacing-lg);">
            <div class="flex justify-between items-start mb-sm">
              <span class="badge badge-ai">Expertise Match: ${trainer.matchScore}%</span>
            </div>
            <p class="text-sm text-muted mb-md">
              <strong class="text-neutral">Competencies Covered:</strong><br>
              ${trainer.expertise}
            </p>
            <div style="background-color: var(--bg-canvas); padding: var(--spacing-sm); border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
              <div class="text-xs font-weight-bold text-secondary mb-xs">Why this trainer matches:</div>
              <p class="text-xs text-muted" style="margin: 0;">
                Strong expertise in Time-Series Forecasting and Python-based analytics, directly aligning with your high-priority skill gap.
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
