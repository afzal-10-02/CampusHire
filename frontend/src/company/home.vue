<script setup>
import apiClient from '@/api';
import StudentNav from '@/components/StudentNav.vue';
import { onMounted } from 'vue';
import { ref } from 'vue';


const data = ref({})

const getData = async () => {
    try {
        const response = await apiClient.get('/api/company/dashboard');
        console.log(response.data)
        if (response.data.status === 'success') {
            data.value = response.data.data;
        } else {
            alert('Failed to fetch dashboard statistics.');
        }
    } catch (error) {
        console.error('Dashboard error:', error);
        alert('An error occurred while loading dashboard data.');
    }
};

onMounted( () =>{
    getData()
})



</script>


<template>

    <StudentNav iscompany="true"/>
  <div class="container my-4">
    

    <!-- DRIVE STATS ROW -->
    <div class="mb-5">
      <h5 class="text-secondary mb-3">Drive Statistics</h5>
      <div class="row g-3">
        
        <div class="col-md-2">
          <div class="card p-3 text-center bg-light">
            <small class=" d-block">Total Drives</small>
            <h3 class="fw-bold text-muted m-0">{{ data?.drive_numbers?.total_drive || 0 }}</h3>
          </div>
        </div>

        <div class="col-md-2">
          <div class="card p-3 text-center bg-light">
            <small class=" d-block">Active</small>
            <h3 class="fw-bold text-success m-0">{{ data?.drive_numbers?.active_drive || 0 }}</h3>
          </div>
        </div>

        <div class="col-md-2">
          <div class="card p-3 text-center bg-light">
            <small class="d-block">Pending</small>
            <h3 class="fw-bold text-warning  m-0">{{ data?.drive_numbers?.pending_drive || 0 }}</h3>
          </div>
        </div>

        <div class="col-md-2">
          <div class="card p-3 text-center bg-light">
            <small class=" d-block">Completed</small>
            <h3 class="fw-bold text-info m-0">{{ data?.drive_numbers?.completed_drive || 0 }}</h3>
          </div>
        </div>

        <div class="col-md-2">
          <div class="card p-3 text-center bg-light">
            <small class=" d-block">Rejected</small>
            <h3 class="fw-bold  text-danger m-0">{{ data?.drive_numbers?.rejected_drive || 0 }}</h3>
          </div>
        </div>

      </div>
    </div>

    <div>
      <h5 class="text-secondary mb-3">Application Statistics</h5>
      <div class="row g-3">

        <div class="col-md-3">
          <div class="card p-3 bg-light">
            <span class=" small">Total Applied</span>
            <h4 class="fw-bold text-muted m-0">{{ data?.application_numbers?.total_applied || 0 }}</h4>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card p-3 bg-light border-start">
            <span class=" small">Shortlisted</span>
            <h4 class="fw-bold text-success m-0">{{ data?.application_numbers?.shortlisted || 0 }}</h4>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card p-3 bg-light border-start">
            <span class="text-warning small">Pending Review</span>
            <h4 class="fw-bold text-warning  m-0">{{ data?.application_numbers?.pending || 0 }}</h4>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card p-3 bg-light border-start">
            <span class="text-danger small">Rejected</span>
            <h4 class="fw-bold text-danger m-0">{{ data?.application_numbers?.rejected || 0 }}</h4>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>


<style scoped>
</style>
