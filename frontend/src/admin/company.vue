<script setup>
import apiClient from '@/api';
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router'
import AdminNav from '@/components/AdminNav.vue';
import Drives from './drives.vue';

const route = useRoute()
const companyId = parseInt(route.params.id)


const data = ref({
  companyData: {
  name: "",
  hr_phone : "",
  hr_name: "",
  hr_email: "",
  description : "",
  email : "", 
  website : "",
  address :""}
})


const numbers = ref({
  total : 0,
  completed: 0,
  active: 0,
  rejected: 0,
  pending: 0
})

const getnumbers = () => {
  const placementData = data.value.placementData;
  
  // 3. Compute counts cleanly with safe fallbacks
  const completedCount = placementData.completed?.length || 0;
  const rejectedCount  = placementData.rejected?.length || 0;
  const activeCount    = placementData.active?.length || 0;
  const pendingCount   = placementData.pending?.length || 0;

  // 4. Update the reactive state fields
  numbers.value.completed = completedCount;
  numbers.value.rejected  = rejectedCount;
  numbers.value.active    = activeCount;
  numbers.value.pending   = pendingCount;
  
  // 5. Calculate and apply the total sum
  numbers.value.total = completedCount + rejectedCount + activeCount + pendingCount;

}

const getdata = async () => {
  try {
    const response = await apiClient.get(`/api/admin/get-company/${companyId}`)

    if (response.status == 200) {
      data.value = response.data.data
      console.log(data)
      getnumbers()
    }
  }
  catch (error) {
    alert("Internal Server Error, Try Again...")
  }
}

onMounted(() => {
  getdata()
})


const corporateDrives = ref([
  { uid: 201, companyName: 'Nexus Tech Solutions', jobDescription: 'Hiring Graduate Software Engineers for full-stack core services.', recruitmentStatus: 'Active', hrManager: 'Sarah Jenkins', hrEmail: 's.jenkins@nexustech.corp', hrPhone: '+1 (555) 019-2834', hqAddress: '101 Innovation Hub, Silicon Valley', corporateUrl: 'https://example.com' },
  { uid: 202, companyName: 'Vanguard Banking Group', jobDescription: 'Recruiting Associate Financial Analysts for global risk management teams.', recruitmentStatus: 'Active', hrManager: 'Marcus Vance', hrEmail: 'm.vance@vanguardbank.com', hrPhone: '+1 (555) 014-9981', hqAddress: '55 Financial District, New York', corporateUrl: 'https://example.com' },
  { uid: 203, companyName: 'Apex Medical Systems', jobDescription: 'Completed drive for Senior Data Scientists in the R&D bio-informatics wing.', recruitmentStatus: 'Completed', hrManager: 'Dr. Elena Rostova', hrEmail: 'e.rostova@apexmed.org', hrPhone: '+1 (555) 017-4422', hqAddress: '89 Health Parkway, Boston', corporateUrl: 'https://example.com' },
  { uid: 204, companyName: 'Horizon Logistics Inc.', jobDescription: 'Drive temporarily blocked due to internal structural reallocation scheduling.', recruitmentStatus: 'Blocked', hrManager: 'David Kross', hrEmail: 'd.kross@horizonlogistics.com', hrPhone: '+1 (555) 012-7733', hqAddress: '304 Supply Route, Chicago', corporateUrl: 'https://example.com' },
]);

const focusedCompany = ref(corporateDrives.value[0]);


const getStatusBadge = (status) => {
  if (status === 'Pending') return 'bg-primary';
  if (status === 'Approved') return 'bg-success';
  if (status === 'Rejected') return 'bg-danger';
  return 'bg-secondary';
};





</script>


<template>
  <AdminNav />

  <div class="container-fluid py-2 my-4 bg-light ">
    <!-- Master Grid Wrapper: Splits Left Profile from Right Metric Cards Panel -->
    <div class="row g-4 align-items-stretch">
      
      <!-- LEFT SIDE PANEL: Detailed Company Profile Info (Fills the wide box) -->
      <div class="col-lg-8">
        <div class="card border-secondary h-100 shadow-sm">
          <div class="card-body p-4 d-flex flex-column justify-content-between">

            
            <div class="row mb-4">
              <div class="col-md-8">
                <h4 class="fw-bold text-dark mb-2">
                  {{ data?.companyData?.name || 'Loading Company...' }}
                </h4>
                <div class="mt-3">
                  <strong class="text-secondary d-block mb-1">Company Description:</strong>
                  <p class="text-muted mb-0">{{ data?.companyData?.description || 'No description provided.' }}</p>
                </div>
              </div>
              <div class="col-md-4 text-md-end mt-3 mt-md-0">
                <span :class="getStatusBadge(data?.companyData?.status)" class="badge px-3 py-2 fs-6">
                  Status: {{ data?.companyData?.status || 'N/A' }}
                </span>
              </div>
            </div>

            <!-- Middle Segment: Dedicated HR Details Box -->
            <div class="p-3 my-3 bg-light border border-secondary rounded shadow-sm">
              <h6 class="fw-bold text-uppercase tracking-wider text-secondary mb-2 small">
                HR Details
              </h6>
              <div class="row text-dark">
                <div class="col-md-4 mb-2 mb-md-0">
                  <span class="text-muted d-block small">HR Name</span>
                  <span class="fw-semibold">{{ data?.companyData?.hr_name || 'N/A' }}</span>
                </div>
                <div class="col-md-4 mb-2 mb-md-0">
                  <span class="text-muted d-block small">Email Address</span>
                  <a :href="'mailto:' + data?.companyData?.hr_email" class="text-decoration-none fw-semibold">
                    {{ data?.companyData?.hr_email || 'N/A' }}
                  </a>
                </div>
                <div class="col-md-4">
                  <span class="text-muted d-block small">Phone Number</span>
                  <span class="fw-semibold">{{ data?.companyData?.hr_phone || 'N/A' }}</span>
                </div>
              </div>
            </div>

            <!-- Bottom Segment: HQ Address & External Links -->
            <div class="row pt-3 border-top border-light-subtle align-items-center">
              <div class="col-sm-7 mb-2 mb-sm-0">
                <p class="mb-0 text-truncate"><strong>HQ Address:</strong> {{ data?.companyData?.address || 'N/A' }}</p>
              </div>
              <div class="col-sm-5 d-flex justify-content-sm-end">
                <p class="mb-0">
                  <strong>Website:</strong>
                  <a :href= "`https://www.${data?.companyData?.website}`" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-dark ms-2 fw-semibold">
                    Visit Portal
                  </a>
                </p>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- RIGHT SIDE PANEL: Metric Cards Layout Structure -->
      <div class="col-lg-4 d-flex flex-column gap-3">
        
        <!-- Row 1: Full-Width Total Card (Top right box in wireframe) -->
        <div class="flex-grow-1">
          <div class="card h-100 border-secondary shadow-sm">
            <div class="card-body p-3 d-flex flex-column justify-content-center">
              <small class="text-uppercase fw-bold text-muted d-block mb-1">Total Drives</small>
              <h3 class="fw-bold m-0 text-dark">{{ numbers.total }}</h3>
            </div>
          </div>
        </div>

        <!-- Row 2: 2 Column Split Grid (Middle pair of wireframe boxes) -->
        <div class="row g-3 flex-grow-1 m-0 p-0">
          <div class="col-6 ps-0">
            <div class="card h-100 border-secondary shadow-sm">
              <div class="card-body p-3">
                <small class="text-uppercase fw-bold text-muted d-block mb-1">Completed</small>
                <h3 class="fw-bold m-0 text-dark">{{ numbers.completed }}</h3>
              </div>
            </div>
          </div>
          <div class="col-6 pe-0">
            <div class="card h-100 border-secondary shadow-sm">
              <div class="card-body p-3">
                <small class="text-uppercase fw-bold text-muted d-block mb-1">Pending</small>
                <h3 class="fw-bold m-0 text-dark">{{ numbers.pending }}</h3>
              </div>
            </div>
          </div>
        </div>

        <!-- Row 3: 2 Column Split Grid (Bottom pair of wireframe boxes) -->
        <div class="row g-3 flex-grow-1 m-0 p-0">
          <div class="col-6 ps-0">
            <div class="card h-100 border-secondary shadow-sm">
              <div class="card-body p-3">
                <small class="text-uppercase fw-bold text-muted d-block mb-1">Active</small>
                <h3 class="fw-bold m-0 text-dark">{{ numbers.active }}</h3>
              </div>
            </div>
          </div>
          <div class="col-6 pe-0">
            <div class="card h-100 border-secondary shadow-sm">
              <div class="card-body p-3">
                <small class="text-uppercase fw-bold text-muted d-block mb-1">Rejected</small>
                <h3 class="fw-bold m-0 text-dark">{{ numbers.rejected }}</h3>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>

  <Drives :isChild ="true" :companyId="companyId" />



</template>


<style scoped>
/* Exact replication of your wireframe's boxy, heavy borders using custom classes */
.border-secondary {
  border: 2px solid #343a40 !important;
  border-radius: 4px !important;
}

.card-header {
  border-bottom: 2px solid #343a40 !important;
}

.tracking-wider {
  letter-spacing: 0.05em;
}

</style>
