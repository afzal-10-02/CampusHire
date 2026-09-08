<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import AdminNav from '@/components/AdminNav.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const driveId = route.params.id;


const driveDetails = ref({
    id: null,
    job_title: "",
    job_description: "",
    min_cgpa: null,
    eligible_year: "",
    status: "",
    application_deadline: ""
});

const numbers = ref({
    total: 0,
    shortlisted: 0,
    rejected: 0,
    pending: 0
})

const appliedStudents = ref({
    applied: [],
    shortlisted: [],
    rejected: []
});


const isloading = ref(false);

const getStatusBadge = (status) => {
    if (status === 'shortlisted') return 'bg-success';
    if (status === 'rejected') return 'bg-danger';
    return 'bg-warning text-dark';
};


const getdata = async () => {
    isloading.value = true;
    try {
        const response = await apiClient.get(`/api/admin/get-drive-details/${driveId}`);
        if (response.data.status === 'success') {
            numbers.value = response.data.numbers;
            driveDetails.value = response.data.drive_details;
            appliedStudents.value = response.data.applied_students;
        }
    } catch (error) {
        if (error.response){
            alert(error.response.data.message)
        }
        console.error('Error fetching drive details:', error);
    } finally {
        isloading.value = false;
    }
};

onMounted(() => {
    getdata();
});

</script>

<template>
    <AdminNav />

    <div class="container py-4">

        <div class="row g-3">

            <!-- LEFT: Drive Details -->
            <div class="col-lg-7">
                <div class=" rounded shadow-sm bg-white h-100">
                    <div class="border-bottom p-3 bg-light">
                        <span class="fw-semibold fs-6">Drive Details</span>
                    </div>

                    <div class="p-4">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div> 
                                <span class="text-muted d-block bold fw-bold">Job Title:</span>
                                <h3 class="fw-bold mb-1">{{ driveDetails.job_title }}</h3>
                            </div>
                            <span class="badge bg-primary px-3 py-2">{{ driveDetails.status }}</span>
                        </div>

                        <div class="mb-3">
                            <span class="text-muted d-block small fw-bold">Description</span>
                            <p class="mb-0">{{ driveDetails.job_description }}</p>
                        </div>

                        <div class="row g-3">
                            <div class="col-sm-4">
                                <span class="text-muted d-block small fw-bold">Min CGPA</span>
                                <span>{{ driveDetails.min_cgpa }}</span>
                            </div>
                            <div class="col-sm-4">
                                <span class="text-muted d-block small fw-bold">eligible_year</span>
                                <span>{{ driveDetails.eligible_year }}</span>
                            </div>
                            <div class="col-sm-4">
                                <span class="text-muted d-block small fw-bold">Deadline</span>
                                <span>{{ driveDetails.application_deadline }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- RIGHT: Stat Cards -->
            <div class="col-lg-5">
                <div class="row g-3">
                    <div class="col-6">
                        <div class="border rounded shadow-sm bg-white p-3 text-center h-100">
                            <span class="text-uppercase text-muted small fw-bold d-block mb-1">Total Applied</span>
                            <h3 class="fw-bold mb-0">{{ numbers.total }}</h3>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="border rounded shadow-sm bg-white p-3 text-center h-100">
                            <span class="text-uppercase text-muted small fw-bold d-block mb-1">Pending Review</span>
                            <h3 class="fw-bold mb-0">{{ numbers.pending }}</h3>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="border rounded shadow-sm bg-white p-3 text-center">
                            <span class="text-uppercase text-muted small fw-bold d-block mb-1">Selected</span>
                            <h3 class="fw-bold mb-0 text-success">{{ numbers.shortlisted }}</h3>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="border rounded shadow-sm bg-white p-3 text-center">
                            <span class="text-uppercase text-muted small fw-bold d-block mb-1">Rejected</span>
                            <h3 class="fw-bold mb-0 text-danger">{{ numbers.rejected }}</h3>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <!-- Applied Students -->
        <div class="border rounded shadow-sm bg-white mt-3">
            <div class="border-bottom p-3 bg-light">
                <span class="fw-semibold fs-6">Applied Students</span>
            </div>

            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th scope="col" class="ps-4">Full Name</th>
                            <th scope="col">Roll Number</th>
                            <th scope="col" class="text-end pe-4">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="isloading">
                            <td colspan="3" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </td>
                        </tr>

                        <tr v-else-if="numbers.total === 0">
                            <td colspan="3" class="text-center text-muted py-4">No students have applied yet.</td>
                        </tr>

                        <template v-else>
                            <tr v-for="student in appliedStudents.applied" :key="'applied-' + student.id">
                                <td class="fw-semibold text-secondary ps-4">{{ student.name }}</td>
                                <td class="text-secondary">{{ student.roll_no }}</td>
                                <td class="text-end pe-4">
                                    <span class="badge px-3 py-2" :class="getStatusBadge('pending')">
                                        Pending
                                    </span>
                                </td>
                            </tr>

                            <tr v-for="student in appliedStudents.shortlisted" :key="'shortlisted-' + student.id">
                                <td class="fw-semibold text-secondary ps-4">{{ student.name }}</td>
                                <td class="text-secondary">{{ student.roll_no }}</td>
                                <td class="text-end pe-4">
                                    <span class="badge px-3 py-2" :class="getStatusBadge('shortlisted')">
                                        Shortlisted
                                    </span>
                                </td>
                            </tr>

                            <tr v-for="student in appliedStudents.rejected" :key="'rejected-' + student.id">
                                <td class="fw-semibold text-secondary ps-4">{{ student.name }}</td>
                                <td class="text-secondary">{{ student.roll_no }}</td>
                                <td class="text-end pe-4">
                                    <span class="badge px-3 py-2" :class="getStatusBadge('rejected')">
                                        Rejected
                                    </span>
                                </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<style scoped></style>