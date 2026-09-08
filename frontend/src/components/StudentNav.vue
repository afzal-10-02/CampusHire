<script setup>
import { ref } from 'vue';

const props = defineProps({
  iscompany: {
    type: Boolean,
    required: true,
    default: false
  },
  name: { 
    type : String,
    required: true,
    default: "user"
  }
})
const user_name = localStorage.getItem("name")
 
</script>
<template>
    <!-- 1. Changed justify-content-center to justify-content-between -->
    <!-- 2. Added align-items-center to keep everything vertically aligned -->
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 bg-light p-3 rounded shadow-sm">

        <div>
            <!-- Added a class to ensure text sizes up nicely like a navbar brand -->
            <p class="mb-0 fw-semibold fs-5 text-dark">
                Hello, {{ user_name }}
            </p>
        </div>
        
        <div v-if="props.iscompany" class="d-flex gap-2">
            <router-link to="/company/home" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                Dashboard
            </router-link>

            <router-link to="/company/drives" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                Drives
            </router-link>


            <router-link to="/company/edit-profile" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                Edit Profile
            </router-link>

            <router-link v-if="!iscompany" to="/company/history" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                History
            </router-link>
        </div>


        <!-- Added d-flex and gap-2 to the links wrapper to space the buttons nicely -->
        <div v-else class="d-flex gap-2">
            <router-link to="/" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                Dashboard
            </router-link>


            <router-link to="/user/edit-profile" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                Edit Profile
            </router-link>

            <router-link to="/user/history" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
                History
            </router-link>
        </div>

    </div>
</template>


<style scoped></style>