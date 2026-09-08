<script setup>
import apiClient from '@/api';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router'
import StudentNav from '@/components/StudentNav.vue';

const route = useRoute()
const companyId = parseInt(route.params.id)
const isshowDrive = ref(false)


const driveDetails = ref({})

const showDrive = async (id) => {
    isshowDrive.value = true

    try {
        const response = await apiClient.get(`/api/user/get-drive/${id}`)
        if (response.data.status === "success") {
            console.log(response.data.data)
            driveDetails.value = response.data.data;
        }
        else {
            alert("Drive Details Loading Failed...")
        }

    } catch (error) {
        if (error.response) {
            alert(error.response.data.message)
        }
        else {
            alert("Internal Server Error, Try Again...")
        }
    }
}


const applyDrive = async (driveId) => {
    const confirmed = confirm("Are you sure you want to apply for this drive?");
    if (!confirmed) return;

    try {
        const response = await apiClient.get(`/api/user/apply-drive/${driveId}`);
        if (response.data.status === "success") {
            alert("Applied Successfully!")
        } else {
            alert(response.data.message)
        }
    } catch (error) {
        if(error.response){
            console.log(error.response)
            alert(error.response.data.message )
        }
        else{
            alert("Internal Server Error, Try Again...")
        }
        
    }
};



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

const activeDrive = ref([])

const getdata = async () => {
  try {
    const response = await apiClient.get(`/api/user/get-company/${companyId}`)

    if (response.status == 200) {
      data.value = response.data.data
      activeDrive.value = response.data.data.active_drives;
      console.log(data)
    }
  }
  catch (error) {
    alert("Internal Server Error, Try Again...")
  }
}

onMounted(() => {
  getdata()
})





</script>


<template>
  <StudentNav />

  <div class="container-fluid py-2 my-4 ">

    <div class="row g-4 align-items-strech justify-content-center">
      
      <div class="col-lg-8">
        <div class="card border-secondary h-100 shadow-sm">
          <div class="card-body p-4 d-flex flex-column justify-content-between bg-light">

            
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
            </div>

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

       <div class="col-lg-3 border-secondary ms-1 d-flex flex-column gap-3 ">

        <table class="table table-hover align-middle mb-0 bg-light">
                    <thead class="table-light">
                        <tr>
                            <th scope="col" class="ps-4">Drive Name</th>

                            <th scope="col" class="text-end pe-4">Actions</th>
                        </tr>
                    </thead>

    
    

                    <tbody>
                        <tr v-if="activeDrive?.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No Active Drives.</td>
                        </tr>
                        <tr v-for="drive in activeDrive" :key="drive.id">
                            <td class="fw-semibold text-secondary ps-4">{{ drive.job_title }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex text-danger">
                                    
                                       <i @click="showDrive(drive.id)" class="fa-xl fa-solid fa-eye text-primary" title="View Drive"></i>
                                    
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

      </div>


     

    </div>


    

  </div>


  
    <div v-if="isshowDrive"
        class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
        style="z-index: 9998; background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(4px);"
        @click.self="showDetails = false">

        <div class="p-4 bg-dark text-white rounded-3 shadow"
            style="max-width: 500px; width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;">

            <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="fw-bold mb-0">{{ driveDetails.job_title }} </h5>
                <span class="badge bg-success px-3 py-2">{{ driveDetails.status }}</span>
            </div>
            <div>
                                <span class="text-white-50 d-block small fw-bold">Company Name</span>

                            <span class=" d-block mb-3">{{ driveDetails.company_name }}</span>

            </div>

            <div class="mb-3">
                <span class="text-white-50 d-block small fw-bold">Description</span>
                <p class="mb-0">{{ driveDetails.job_description }}</p>
            </div>

            <div class="row g-3 mb-3">
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Eligible Branch</span>
                    <span>{{ driveDetails.eligible_branches }}</span>
                </div>
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Eligible Year</span>
                    <span>{{ driveDetails.eligible_year }}</span>
                </div>
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Min CGPA</span>
                    <span>{{ driveDetails.min_cgpa }}</span>
                </div>
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Application Deadline</span>
                    <span>{{ driveDetails.application_deadline }}</span>
                </div>
            </div>

            <hr class="border-secondary">

            <div class="mb-3">
                <span class="text-white-50 d-block small fw-bold mb-2">HR Contact</span>
                <div class="row g-2">
                    <div class="col-sm-4">
                        <span class="text-white-50 d-block small">Name</span>
                        <span>{{ driveDetails.hr_name }}</span>
                    </div>
                    <div class="col-sm-4">
                        <span class="text-white-50 d-block small">Email</span>
                        <span class="text-break">{{ driveDetails.hr_email }}</span>
                    </div>
                    <div class="col-sm-4">
                        <span class="text-white-50 d-block small">Phone</span>
                        <span>{{ driveDetails.hr_phone }}</span>
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-end pt-1">
                <button @click="isshowDrive = false" type="button"
                    class="btn btn-sm btn-light px-3 border-1">Close</button>
                    <button @click="applyDrive(driveDetails.id)" type="button"
                    class="btn btn-sm ms-2 bg-success px-3 border-1">Apply</button>
            </div>
        </div>
    </div>


</template>


<style scoped>
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
