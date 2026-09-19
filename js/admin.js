const AdminDashboard = {
  init: async function() {
    await this.fetchMetrics();
    await this.fetchPendingTrainers();
  },

  fetchMetrics: async function() {
    try {
      const data = await window.api.get('/admin/metrics');
      if (data && data.metrics) {
        document.getElementById('admin-kpi-trainees').textContent = data.metrics.total_trainees ?? 0;
        document.getElementById('admin-kpi-trainers').textContent = data.metrics.total_trainers ?? 0;
        document.getElementById('admin-kpi-pending').textContent = data.metrics.pending_trainers ?? 0;
      }
    } catch (e) {
      console.error("Failed to load admin metrics", e);
    }
  },

  fetchPendingTrainers: async function() {
    const tbody = document.getElementById('pending-trainers-table');
    if (!tbody) return;

    try {
      const trainers = await window.api.get('/admin/pending-trainers');
      if (!trainers || !trainers.length) {
        tbody.innerHTML = `
          <tr>
            <td colspan="4" style="padding: var(--spacing-md); text-align: center;" class="text-muted">
              No pending trainer applications found.
            </td>
          </tr>
        `;
        return;
      }

      let html = '';
      trainers.forEach(t => {
        html += `
          <tr style="border-bottom: 1px solid var(--border-default);">
            <td style="padding: var(--spacing-md) var(--spacing-sm); font-weight: 600; color: var(--color-primary);">${t.name}</td>
            <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">${t.email}</td>
            <td style="padding: var(--spacing-md) var(--spacing-sm);"><span class="badge badge-warning">${t.status}</span></td>
            <td style="padding: var(--spacing-md) var(--spacing-sm);">
              <button class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: var(--text-xs);" onclick="AdminDashboard.approveTrainer('${t.id}')">Approve</button>
              <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: var(--text-xs); color: var(--color-danger);" onclick="AdminDashboard.rejectTrainer('${t.id}')">Reject</button>
            </td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    } catch (e) {
      console.error("Failed to fetch pending trainers", e);
    }
  },

  approveTrainer: async function(trainerId) {
    try {
      await window.api.put(`/admin/trainers/${trainerId}/approve`, {});
      alert("Trainer approved successfully!");
      this.init();
    } catch (e) {
      alert("Approval failed: " + e.message);
    }
  },

  rejectTrainer: async function(trainerId) {
    try {
      await window.api.put(`/admin/trainers/${trainerId}/reject`, {});
      alert("Trainer rejected.");
      this.init();
    } catch (e) {
      alert("Rejection failed: " + e.message);
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('pending-trainers-table')) {
    AdminDashboard.init();
  }
});
