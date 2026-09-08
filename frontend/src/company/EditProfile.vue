<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api'
import StudentNav from '@/components/StudentNav.vue';

const loading = ref(false)
const msg = ref("");

const editfield = ref({
  show: false,
  name: '',
  data: ''
})


const companyData = ref({
  email: '',
  status: '',
  name: '',
  description: '',
  address: '',
  hr_name: '',
  hr_email: '',
  hr_phone: '',
  website: ''
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
    const response = await apiClient.put(`/api/company/update-profile`, payload)
    if (response.data.status === "success") {
      msg.value = response.data.message;
      getCompanyData()
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


const getCompanyData = async () => {
  try {
    const response = await apiClient.get(`/api/company/update-profile`)
    if (response.data.status === "success") {
      companyData.value = response.data.data
    } else {
      console.error("Failed to fetch company data:", response.data.message)
    }
  } catch (error) {
    console.error("Error fetching company data:", error)
  }
}

const getStatusBadge = (status) => {
  if (status === 'Pending') return 'bg-primary';
  if (status === 'Approved') return 'bg-success';
  if (status === 'Rejected') return 'bg-danger';
  return 'bg-secondary';
};

onMounted(() => {
  getCompanyData()
})


</script>

<template>
        <StudentNav iscompany=true />


  <div class="container my-5" style="max-width: 700px;">
    <div class="card shadow-sm border-0">
      <!-- Header -->
      <div class="card-header bg-dark text-white py-3">
        <h5 class="mb-0 fw-bold">Company Profile Details</h5>
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
              <span class="text-dark fw-medium">{{ companyData.email }}</span>
            </div>
            <div class="col-sm-6">
              <span :class="getStatusBadge(companyData?.status)" class="badge px-3 py-2 fs-6">
                  Status: {{ companyData?.status || 'N/A' }}
                </span>
            </div>
          </div>
        </div>

        <!-- SECTION 2: Company Details -->
        <div class="mb-4">
          <h6 class="text-uppercase text-secondary fw-bolder tracking-wider border-bottom pb-2 mb-3"
            style="font-size: 0.8rem;">
            Company Details
          </h6>
          <div class="row g-3">
            <div class="col-sm-6">
              <span class="text-muted d-block small fw-bold">Company Name</span>
              <span class="text-dark fw-medium">{{ companyData.name }}</span>
            </div>
            <div class="col-sm-6">
              <span class="text-muted d-block small fw-bold">Website</span>
              <span class="text-dark fw-medium">{{ companyData.website || '—' }}</span>
            <i class="fa-solid fa-pencil mx-2" @click="handleEdit('website', companyData.website)"> </i>

            </div>
            <div class="col-12">
              <span class="text-muted d-block small fw-bold">Description</span>
              <span class="text-dark fw-medium">{{ companyData.description || '—' }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('description', companyData.description)"> </i>
            </div>
            <div class="col-12">
              <span class="text-muted d-block small fw-bold">Address</span>
              <span class="text-dark fw-medium">{{ companyData.address || '—' }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('address', companyData.address)"> </i>
            </div>
          </div>
        </div>

        <div>
          <h6 class="text-uppercase text-secondary fw-bolder tracking-wider border-bottom pb-2 mb-3"
            style="font-size: 0.8rem;">
            HR Details
          </h6>
          <div class="row g-3">
            <div class="col-sm-4">
              <span class="text-muted d-block small fw-bold">HR Name</span>
              <span class="text-dark fw-medium">{{ companyData.hr_name || '—' }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('hr_name', companyData.hr_name)"> </i>
            </div>

            <div class="col-sm-4">
              <span class="text-muted d-block small fw-bold">HR Email</span>
              <span class="text-dark fw-medium">{{ companyData.hr_email || '—' }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('hr_email', companyData.hr_email)"> </i>
            </div>

            <div class="col-sm-4">
              <span class="text-muted d-block small fw-bold">HR Phone</span>
              <span class="text-dark fw-medium">{{ companyData.hr_phone || '—' }}</span>
              <i class="fa-solid fa-pencil mx-2" @click="handleEdit('hr_phone_number', companyData.hr_phone)"> </i>
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