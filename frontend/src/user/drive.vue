<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import AdminNav from '@/components/AdminNav.vue';
import { useRoute } from 'vue-router';
import StudentNav from '@/components/StudentNav.vue';

const route = useRoute();
const driveId = route.params.id;


const driveDetails = ref({});



const getData = async () => {

    try {
        const response = await apiClient.get(`/api/user/get-drive/${driveId}`)
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
        if (error.response) {
            alert(error.response.data.message)
        }
        else {
            alert("Internal Server Error, Try Again...")
        }

    }
};



onMounted(() => {
    getData();
});

</script>
<template>
    <StudentNav />

    <!-- Centered container taking exactly 75% width of the viewport -->
    <div class="container w-75 my-5">

        <!-- Main Drive Details Box with light theme styling -->
        <div class="card bg-light text-dark border-0 rounded-3 shadow-sm p-4">

            <!-- Header Section with Job Title and Status Badge -->
            <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
                <div>
                    <h3 class="fw-bold text-dark mb-1">{{ driveDetails.job_title }}</h3>
                    <div class="d-flex align-items-center gap-2">
                        <span class="text-secondary small fw-semibold">Company:</span>
                        <span class="fw-bold text-primary">{{ driveDetails.company_name }}</span>
                    </div>
                </div>
                <span
                    class="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 rounded-pill fw-semibold">
                    {{ driveDetails.status }}
                </span>
            </div>

            <!-- Job Description Block -->
            <div class="mb-4">
                <span class="text-muted d-block small text-uppercase tracking-wider fw-bold mb-1">Job Description</span>
                <p class="text-secondary mb-0lh-base">{{ driveDetails.job_description }}</p>
            </div>

            <!-- Eligibility Criteria Grid Layout -->
            <div class="bg-white border rounded-3 p-3 mb-4 shadow-sm">
                <span class="text-muted d-block small text-uppercase tracking-wider fw-bold mb-3">Eligibility
                    Criteria</span>
                <div class="row g-3">
                    <div class="col-sm-6 col-md-3">
                        <span class="text-muted d-block small">Eligible Branch</span>
                        <span class="fw-semibold text-dark">{{ driveDetails.eligible_branches }}</span>
                    </div>
                    <div class="col-sm-6 col-md-3">
                        <span class="text-muted d-block small">Eligible Year</span>
                        <span class="fw-semibold text-dark">{{ driveDetails.eligible_year }}</span>
                    </div>
                    <div class="col-sm-6 col-md-3">
                        <span class="text-muted d-block small">Min CGPA</span>
                        <span class="fw-semibold text-dark">{{ driveDetails.min_cgpa }}</span>
                    </div>
                    <div class="col-sm-6 col-md-3">
                        <span class="text-muted d-block small">Application Deadline</span>
                        <span class="fw-semibold text-danger">{{ driveDetails.application_deadline }}</span>
                    </div>
                </div>
            </div>

            <!-- HR Contact Details Section -->
            <div class="bg-white border rounded-3 p-3 mb-4 shadow-sm">
                <span class="text-muted d-block small text-uppercase tracking-wider fw-bold mb-3">HR Contact
                    Information</span>
                <div class="row g-3">
                    <div class="col-sm-4">
                        <span class="text-muted d-block small">Full Name</span>
                        <span class="fw-semibold text-dark">{{ driveDetails.hr_name }}</span>
                    </div>
                    <div class="col-sm-4">
                        <span class="text-muted d-block small">Email Address</span>
                        <a :href="'mailto:' + driveDetails.hr_email"
                            class="text-decoration-none fw-semibold text-primary text-break">
                            {{ driveDetails.hr_email }}
                        </a>
                    </div>
                    <div class="col-sm-4">
                        <span class="text-muted d-block small">Phone Number</span>
                        <span class="fw-semibold text-dark">{{ driveDetails.hr_phone }}</span>
                    </div>
                </div>
            </div>

            <!-- Action Control Buttons -->
            <div class="d-flex justify-content-end gap-2 border-top pt-3">
                <button @click="applyDrive(driveDetails.id)" type="button"
                    class="btn btn-success px-4 fw-medium shadow-sm">
                    Apply Now
                </button>
            </div>

        </div>
    </div>
</template>


<style scoped></style>