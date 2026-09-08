<script setup>
import { onMounted, ref } from 'vue';
import apiClient from '@/api';
import StudentNav from '@/components/StudentNav.vue';
import router from '@/router';

const isloading = ref(false);
const toast = ref({ status: false, msg: "" });
const cmsg = ref("")
const dmsg = ref("")
const isshowDrive = ref(false)


const viewCompany = async (id) => {
    router.push(`/user/company/${id}`)
}


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



const activeDrives = ref([
    {
        id: null,
        job_title: '',
        deadline: '',
        company_name: ''
    }
]);

const activeCompanies = ref([
    {
        id: null,
        name: ''
    },
]);

const getCompanies = async () => {
    isloading.value = true
    try {
        const response = await apiClient.get("/api/user/get-active-companies");
        if (response.data.status === "success") {
            activeCompanies.value = response.data.data;
        } else {
            cmsg.value = response.data.message
        }
    } catch (error) {
        cmsg.value = response.data.message;
    } finally {
        isloading.value = false;
    }
}

const getDrives = async () => {
    isloading.value = true;
    try {
        const response = await apiClient.get("/api/user/get-active-drives");
        if (response.data.status === "success") {
            activeDrives.value = response.data.data;
        } else {
            dmsg.value = response.data.message;
        }
    } catch (error) {
        toast.value = { status: true, msg: "Something went wrong. Refresh the page..." };
    } finally {
        isloading.value = false;
    }
};

const applyDrive = async (driveId) => {
    const confirmed = confirm("Are you sure you want to apply for this drive?");
    if (!confirmed) return;

    try {
        const response = await apiClient.get(`/api/user/apply-drive/${driveId}`);
        if (response.data.status === "success") {
            toast.value = { status: true, msg: "Applied Successfully!" };
        } else {
            toast.value = { status: true, msg: response.data.message || "Failed to apply." };
        }
    } catch (error) {
        if(error.response){
            console.log(error.response)
            toast.value = { status: true, msg: error.response.data.message };
        }
        else{
            toast.value = {status : true, msg : "Internal Server Error, Try Again..."}
        }
        
    }
};

onMounted(() => {
    getDrives()
    getCompanies()
});

</script>

<template>
    <StudentNav />

    <div class="container py-4">
        <div class="row g-3 justify-content-center">

            <!-- LEFT: Active Drives -->
            <div class="col-lg-8">
                <div class="border rounded shadow-sm bg-white h-100">
                    <div class="border-bottom p-3 text-center bg-light">
                        <span class="fw-bold">Active Drives</span>
                    </div>

                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th scope="col" class="ps-3 pe-0 me-0">Job title(Company)</th>
                                <th scope="col">Deadline</th>
                                <th scope="col" class="text-end pe-4">Actions</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-if="isloading">Loading Companies</tr>
                            <tr v-for="drive in activeDrives" :key="drive.id">
                                <td class="fw-semibold text-secondary ps-3 pe-0 me-0">{{ drive.job_title }} ({{
                                    drive.company_name }} )</td>
                                <td class="text-secondary">{{ drive.application_deadline }}</td>
                                <td class="text-end pe-4">

                                    <i @click="showDrive(drive.id)" class="fa-xl fa-solid fa-eye text-primary me-2"
                                        title="View Drive"></i>

                                    <button @click="applyDrive(drive.id)" class="btn btn-success btn-sm px-3">
                                        Apply
                                    </button>
                                </td>
                            </tr>
                        </tbody>




                    </table>
                </div>
            </div>

            <!-- RIGHT: Companies -->
            <div class="col-lg-4">
                <div class="border rounded shadow-sm bg-white h-100">
                    <div class="border-bottom p-3 text-center bg-light">
                        <span class="fw-semibold">Companies</span>
                    </div>

                    <ul class="list-group list-group-flush">
                        <span v-for="company in activeCompanies" :key="company.id" class="list-group-item text-center">
                            <li @click="viewCompany(company.id)" class="text-primary list-group-item cursor-pointer">{{
                                company.name }} </li>
                        </span>
                    </ul>
                </div>
            </div>

        </div>
    </div>

    <div v-if="toast.status"
        class="position-fixed top-50 start-50 translate-middle bg-dark text-white px-4 py-3 rounded shadow d-flex align-items-center gap-3"
        style="z-index: 9999;">
        <span>{{ toast.msg }}</span>
        <button @click="toast.status = false" type="button" class="btn-close btn-close-white"
            aria-label="Close"></button>
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
                    <span class="text-danger">{{ driveDetails.application_deadline }}</span>
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
.cursor-pointer {
    cursor: pointer !important;
}
</style>