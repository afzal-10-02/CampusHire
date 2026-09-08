<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import { useRoute } from 'vue-router';
import AdminNav from '@/components/AdminNav.vue';

const route = useRoute();
const studentId = route.params.id;

const student = ref({
  full_name:  "",
  email: "",
  status: "",
  branch: "",
  cgpa: null,
  roll_number : "",
  graduation_year:  null,
  address: "",
  resume_link: "",
  address: ""
});

const appliedDrives = ref([
  {id: null, job_title: '', status: '' }
]);

const getStudent = async () => {
  try {
    const response = await apiClient.get(`/api/admin/get-students/${studentId}`);
    if (response.status == 200) {
      student.value = response.data.data;
      appliedDrives.value = response.data.appliedDrives;

    }
    else{
        alert(response.data.message)
    }
  } catch (err) {
    console.error('Failed to load student profile:', err);
  }
};

const statusBadgeClass = (status) => {
  const map = {
    Selected: 'badge-selected',
    Shortlisted: 'badge-shortlisted',
    Pending: 'badge-pending',
    Rejected: 'badge-rejected',
    active: 'badge-active',
    blocked : "badge-blocked" 

  };
  return map[status] || 'badge-pending';
};

onMounted(() => {
  getStudent();
});
</script>

<template>
 <AdminNav />

  <div class="profile-page py-4">
    <div class="container-fluid">
      <div class="row g-3">

        <!-- Left Panel: Student Info -->
        <div class="col-lg-7">
          <div class="info-card p-4 h-100">

            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="fw-semibold fs-5 text-name">{{ student.full_name || 'N/A' }}</span>
              <span class="status-pill" :class="statusBadgeClass(student.status)">
                {{ student.status || 'N/A' }}
              </span>
            </div>

            <div class="mb-3">
              <span class="fw-semibold label-muted">Email:</span>
              <span class="ms-2">{{ student.email || 'N/A' }} </span>

              <span class="fw-semibold label-muted ms-5">Roll No.:</span>
              <span class="ms-2">{{ student.roll_number || 'N/A' }} </span>
            </div>

            <div class="detail-strip p-3 mb-3">
              <div class="row">
                <div class="col-4">
                  <span class="fw-semibold d-block label-muted small">Branch</span>
                  <span>{{ student.branch || 'N/A' }}</span>
                </div>
                <div class="col-4">
                  <span class="fw-semibold d-block label-muted small">Cgpa</span>
                  <span>{{ student.cgpa || 'N/A' }}</span>
                </div>
                <div class="col-4">
                  <span class="fw-semibold d-block label-muted small">Graduation</span>
                  <span>{{ student.graduation_year || 'N/A' }}</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <span class="fw-semibold d-block label-muted small">Address</span>
              <span>{{ student.address || 'N/A' }}</span>
            </div>

            <div>
              <span class="fw-semibold d-block label-muted small">Resume Link</span>
              <a :href="student.resume_link" target="_blank" class="resume-link">{{ student.resume_link || 'N/A' }}</a>
            </div>

          </div>
        </div>

        <!-- Right Panel: Drives Applied At -->
        <div class="col-lg-5">
          <div class="drives-card h-100">

            <div class="drives-header p-3">
              <span class="fw-semibold fs-6">Drives Applied At</span>
            </div>

            <table class="table table-borderless mb-0">
              <thead>
                <tr class="table-head-row">
                  <th class="ps-3 label-muted small">Job Title</th>
                  <th class="ps-3 label-muted small">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="appliedDrives.length === 0">
                  <td colspan="2" class="text-center label-muted py-3">No drives applied.</td>
                </tr>
                <tr v-for="drive in appliedDrives" :key="drive.id" class="drive-row">
                  <td class="ps-3">{{ drive.job_title }}</td>
                  <td class="ps-3">
                    <span class="status-pill sm" :class="statusBadgeClass(drive.status)">
                      {{ drive.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  min-height: 100vh;
}

.info-card {
  background-color: #FFFFFF;
  border: 1px solid #DCE3EC;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(20, 40, 70, 0.06);
}

.text-name {
  color: #1F2D3D;
}

.label-muted {
  color: #6B7A90;
}

.detail-strip {
  background-color: #F5F8FC;
  border: 1px solid #E2E9F1;
  border-radius: 8px;
}

.resume-link {
  color: #2E5FA3;
  text-decoration: none;
}
.resume-link:hover {
  text-decoration: underline;
}

.drives-card {
  background-color: #FFFFFF;
  border: 1px solid #DCE3EC;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(20, 40, 70, 0.06);
  overflow: hidden;
}

.drives-header {
  background-color: #1F2D3D;
  color: #FFFFFF;
}

.table-head-row {
  border-bottom: 1px solid #E2E9F1;
}

.drive-row {
  border-bottom: 1px solid #EEF2F7;
}
.drive-row:last-child {
  border-bottom: none;
}

.status-pill {
  display: inline-block;
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}
.status-pill.sm {
  font-size: 0.75rem;
  padding: 0.2rem 0.6rem;
}

.badge-selected {
  background-color: #DFF3E6;
  color: #1E7A46;
}
.badge-shortlisted {
  background-color: #DCEBFB;
  color: #1D5EA8;
}
.badge-pending {
  background-color: #FCF3D9;
  color: #92720F;
}
.badge-rejected {
  background-color: #FBE1E1;
  color: #A32E2E;
}

.badge-active{
    background-color: #DFF3E6;
  color: #1E7A46;
}
.badge-blocked{
     background-color: #FBE1E1;
  color: #A32E2E;
}

</style>