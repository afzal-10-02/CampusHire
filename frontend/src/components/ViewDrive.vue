<script setup>
import apiClient from '@/api';
import { onMounted, ref } from 'vue';



const props = defineProps({
  id: {
    type: Number,
    required: true,
    default : 1
  },
})

const drive = ref({})

const getDrive = async () => {
  try{
    const response = await apiClient.get(`/api/admin/get-drive/${props.id}`)
    if (response.data.status = "success") {
      drive.value = response.data.data;
    }
    else{
      alert(response.data.message)
    }
  }
  catch{
    alert("Internal Server Errror, Try Again..." )
  }

}

onMounted( () =>{
  getDrive()
})

defineEmits(['close'])



</script>

<template>


<div class="modal-overlay">
  <div class="details-card">
    <h3 class="title">Drive Details</h3>
    <hr />

    <div v-if="drive" class="details-body">
      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
      <p><strong>Company Name:</strong> {{ drive.company_name }}</p>
      <p><strong>Status:</strong> <span class="badge bg-success small">{{ drive.status }}</span></p>
      
      <p><strong>Job Description:</strong> {{ drive.job_description }}</p>
      
      <p><strong>Minimum CGPA:</strong> {{ drive.min_cgpa }}</p>
      <p><strong>Eligible Branches:</strong> {{ drive.eligible_branches }}</p>
      <p><strong>Eligible Year:</strong> {{ drive.eligible_year }}</p>
      <p><strong>Application Deadline:</strong> {{ drive.application_deadline }}</p>
      
      <p><strong>HR Contact Name:</strong> {{ drive.hr_name }}</p>
      <p><strong>HR Phone:</strong> {{ drive.hr_phone }}</p>
      <p><strong>HR Email:</strong> {{ drive.hr_email }}</p>
    </div>

    <div class="d-flex justify-content-end mt-4">
      <button class="btn btn-secondary rounded-0" @click="$emit('close')">Close</button>
    </div>
  </div>
</div>




</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(3px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.details-card {
  background: white;
  padding: 30px;
  width: 100%;
  max-width: 500px;
  border-radius: 0px;
  /* Kept square to match your style */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.title {
  text-transform: uppercase;
  font-weight: bold;
}
</style>