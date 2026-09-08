<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import { useRoute } from 'vue-router';
import StudentNav from '@/components/StudentNav.vue';

const route = useRoute();
const driveId = route.params.id;
const isshowStudent = ref(false)

const studentDetails = ref({})

const getstudentDetails = async (id) => {
    try {
        const response = await apiClient.get(`/api/company/get-student/${id}`)
        if (response.data.status === "success") {
            studentDetails.value = response.data.data
            isshowStudent.value = true
        } else {
            alert("Something went wrong, try again")
        }
    } catch {
        alert("Something went wrong, try again")
    }
}

const handleShortlist = async (student_id) => {
    try {
        const response = await apiClient.get(`/api/company/shortlist-student/${student_id}/${driveId}`)
        if (response.data.status == "success") {
            alert("Student Shortlisted")
            getdata()
        }
        else {
            alert(response.data.message)
        }
    }
    catch (error) {
        if (error.response) {
            alert(error.response.data.message)
        }
        else {
            alert("Internal Server Error, try...")

        }
    }
}

const handleReject = async (student_id) => {
    try {
        const response = await apiClient.get(`/api/company/reject-student/${student_id}/${driveId}`)
        if (response.data.status == "success") {
            alert("Student Rejected")
            getdata()
        }
        else {
            alert(response.data.message)
        }
    }
    catch (error) {
        if (error.response) {
            alert(error.response.data.message)
        }
        else {
            alert("Internal Server Error, try...")

        }
    }
}


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
        if (error.response) {
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
    <StudentNav iscompany="true" />

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
                                    <button @click="getstudentDetails(student.id)" class="btn ms-2"> <i
                                            class="fa-xl fa-solid fa-eye text-primary" title="View Drive"></i>
                                    </button>
                                    <span class="badge px-3 py-2 ms-2" :class="getStatusBadge('pending')">
                                        Pending
                                    </span>

                                    <button @click="handleShortlist(student.id)"
                                        class="btn btn-sm btn-success ms-2">Shortlist</button>
                                    <button @click="handleReject(student.id)"
                                        class="btn btn-sm btn-danger ms-2">Reject</button>

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


    <div v-if="isshowStudent"
        class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
        style="z-index: 9998; background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(4px);"
        @click.self="isshowStudent = false">

        <div class="p-4 bg-dark text-white rounded-3 shadow"
            style="max-width: 500px; width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;">

            <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="fw-bold mb-0 text-uppercase">{{ studentDetails.full_name || N / A }}</h5>
                <span class="badge px-3 py-2" :class="studentDetails.status === 'active' ? 'bg-success' : 'bg-danger'">
                    {{ studentDetails.status }}
                </span>
            </div>

            <div class="mb-3">
                <span class="text-white-50 d-block small fw-bold">Roll Number</span>
                <span class="d-block">{{ studentDetails.roll_number }}</span>
            </div>

            <div class="mb-3">
                <span class="text-white-50 d-block small fw-bold">Email</span>
                <span class="d-block text-break">{{ studentDetails.email }}</span>
            </div>

            <div class="row g-3 mb-3">
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Branch</span>
                    <span>{{ studentDetails.branch }}</span>
                </div>
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">CGPA</span>
                    <span>{{ studentDetails.cgpa }}</span>
                </div>
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Graduation Year</span>
                    <span>{{ studentDetails.graduation_year }}</span>
                </div>
                <div class="col-sm-6">
                    <span class="text-white-50 d-block small fw-bold">Address</span>
                    <span>{{ studentDetails.address || 'N/A' }}</span>
                </div>
            </div>

            <hr class="border-secondary">

            <div class="mb-3">
                <span class="text-white-50 d-block small fw-bold">Resume</span>
                <a v-if="studentDetails.resume_link" :href="studentDetails.resume_link" target="_blank"
                    class="text-info text-break">
                    View Resume
                </a>
                <span v-else class="text-white-50">Not uploaded</span>
            </div>

            <div class="d-flex justify-content-end pt-1">
                <button @click="isshowStudent = false" type="button"
                    class="btn btn-sm btn-light px-3 border-1">Close</button>

                <button @click="handleShortlist(student.id)" class="btn btn-sm btn-success ms-2">Shortlist</button>
                <button @click="handleReject(student.id)" class="btn btn-sm btn-danger ms-2">Reject</button>

            </div>
        </div>
    </div>

</template>

<style scoped></style>