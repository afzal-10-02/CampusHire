<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api'
import StudentNav from '@/components/StudentNav.vue'


const loading = ref(false)
const msg = ref("");

const editfield = ref({
  show: false,
  name: '',
  data: ''
})


const studentData = ref({
  email: '',
  status: '',
  roll_number: '',
  full_name: '',
  address: '',
  branch: '',
  cgpa: null,
  graduation_year: null,
  resume_link: ''
})

const handleEdit = (name, value) => {
  editfield.value.show = true;
  editfield.value.name = name;
  editfield.value.data = value;
}

const updateField = async () => {
  loading.value = true
  const payload = {
    name: editfield.value.name,
    data: editfield.value.data
  }

  try {
    const response = await apiClient.put(`/api/user/update-profile`, payload)
    if (response.data.status === "success") {
      msg.value = response.data.message;
      getStudentData()
      console.log(response)
    } else {
      msg.value = response.data.message;
    }
  } catch (error) {
    msg.value = "Server Error. Try Again..."
  }
  finally {
    loading.value = false;
  }

}


const getStudentData = async () => {
  try {
    const response = await apiClient.get(`/api/user/get-profile`)
    if (response.data.status === "success") {
      studentData.value = response.data.data
    } else {
      console.error("Failed to fetch student data:", response.data.message)
    }
  } catch (error) {
    console.error("Error fetching student data:", error)
  }
}

onMounted(() => {
  getStudentData()
})


</script>

<template>
  <StudentNav />

  <div class="container my-5" style="max-width: 700px;">
    <div class="card shadow-sm border-0">
      <!-- Header -->
      <div class="card-header bg-dark text-white py-3">
        <h5 class="mb-0 fw-bold">Student Profile Details</h5>
      </div>

      <div class="card-body p-4 bg-light-grow">

        <!-- SECTION 1: Account Information -->
        <div class="mb-4">
          <h6 class="text-uppercase text-secondary fw-bolder tracking-wider border-bottom pb-2 mb-3"
            style="font-size: 0.8rem;">
            Account Profile
          </h6>
          <div class="row g-3">
            <div class="col-sm-6">
              <span class="text-muted d-block small fw-bold">Email Address</span>
              <span class="text-dark fw-medium">{{ studentData.email }}</span>
            </div>
            <div class="col-sm-6">
              <span class="text-muted d-block small fw-bold">Account Status</span>
              <span
                :class="['badge rounded-pill px-3 py-1.5 mt-1 fs-7', studentData.status === 'active' ? 'bg-success-subtle text-success border border-success-subtle' : 'bg-danger-subtle text-danger border border-danger-subtle']">
                {{ studentData.status }}
              </span>
            </div>
          </div>
        </div>

        <!-- SECTION 2: Personal Profile -->
        <div class="mb-4">
          <h6 class="text-uppercase text-secondary fw-bolder tracking-wider border-bottom pb-2 mb-3"
            style="font-size: 0.8rem;">
            Personal Details
          </h6>
          <div class="row g-3">
            <div class="col-sm-6">
              <span class="text-muted d-block small fw-bold">Roll Number</span>
              <span class="text-dark fw-medium fs-6 text-monospace">{{ studentData.roll_number }}</span>
            </div>
            <div class="col-sm-6">
              <span class="text-muted d-block small fw-bold">Full Name</span>
              <span class="text-dark fw-medium">{{ studentData.full_name || '—' }}</span>
            </div>
            <div class="col-12">
              <span class="text-muted d-block small fw-bold">Current Address</span>
              <span class="text-dark fw-medium">{{ studentData.address || '—' }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('address', studentData.address)"> </i>

            </div>
          </div>
        </div>

        <!-- SECTION 3: Academic Eligibility -->
        <div>
          <h6 class="text-uppercase text-secondary fw-bolder tracking-wider border-bottom pb-2 mb-3"
            style="font-size: 0.8rem;">
            Academic Details 
          </h6>
          <div class="row g-3">
            <div class="col-sm-4">
              <span class="text-muted d-block small fw-bold">Branch</span>
              <span class="text-dark fw-medium">{{ studentData.branch || '—' }}</span>
            </div>

            <div class="col-sm-4">
              <span class="text-muted d-block small fw-bold">Cumulative CGPA</span>
              <span class="text-dark fw-bold text-primary">{{ studentData.cgpa ? studentData.cgpa.toFixed(2) : '—'
              }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('cgpa', studentData.cgpa)"> </i>

            </div>

            <div class="col-sm-4">
              <span class="text-muted d-block small fw-bold">Graduation Year</span>
              <span class="text-dark fw-medium">{{ studentData.graduation_year || '—' }}</span>
            </div>
            <div class="col-12">
              <span class="text-muted d-block small fw-bold">Resume Link</span>
              <div class="mt-1">
                <a v-if="studentData.resume_link" :href="studentData.resume_link" target="_blank"
                  class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1">
                  View Attached Resume ↗
                </a>


                <span v-else class="text-muted italic small">No resume submitted</span>
                <i class="fa-solid fa-pencil mx-2" @click="handleEdit('resume_link', studentData.resume_link)"> </i>

              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>


  <div v-if="editfield.show" class="position-fixed top-0 start-0 w-100 h-100"
    style="z-index: 9998; background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(4px); cursor: not-allowed;">
  </div>



  <div v-if="editfield.show"
    class="position-fixed top-50 start-50 translate-middle w-100 p-4 bg-dark text-white rounded-3 shadow"
    style="z-index: 9999; max-width: 400px; box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;">

    <h6 class="fw-bold mb-1 text-capitalize">Update {{ editfield.name }}</h6>

    <div class="mb-3">
      <input v-model="editfield.data" type="text" class="form-control form-control-sm bg-secondary text-white border-1"
        style="--bs-bg-opacity: 0.2;" />
    </div>

    <p v-if="msg"> {{ msg }}</p>

    <div v-if="loading" class="spinner-border" role="status">
      </div>

    <div class="d-flex justify-content-end gap-2 pt-1">
      <button @click="editfield.show = false; msg = '' "   type="button" class="btn btn-sm btn-light px-3 border-0">Back</button>
      
      <button @click="updateField" class="btn btn-sm btn-light fw-bold px-3">Update</button>
    </div>
  </div>





</template>

<style scoped></style>