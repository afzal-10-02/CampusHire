<script setup>
import { onMounted, ref } from 'vue';
import apiClient from '@/api';
import AdminNav from '@/components/AdminNav.vue';

const active = ref("approved")
const isloading = ref("false")
const alertmsg = ref("")
const toast = ref({ "status": false, "msg": "" })

const handlebtn1 = () => active.value = "approved";
const handlebtn2 = () => active.value = "pending";
const handlebtn3 = () => active.value = "blocked";



const approvedCompanies = ref([])

const pendingCompanies = ref([])

const blockedCompanies = ref([])


const fetchdata = async () => {
    try {
        const response = await apiClient.get("/api/admin/get-companies")


        approvedCompanies.value = response.data.data.approved;
        pendingCompanies.value = response.data.data.pending;
        blockedCompanies.value = response.data.data.rejected;
    }
    catch (error) {
        toast.value = { "status": true, "msg": "Something Went Wrong. Refresh the Page..." }
    }
    finally {
        isloading.value = false;
    }



}

const handleApprove = async (companyId) => {
    const confirmed = confirm("Are You Sure You Want to Approve this Company?");
    if (!confirmed) return;

    try {
        const response = await apiClient.patch(`/api/admin/approve-company/${companyId}`);
        if (response.data.status === "success") {
            toast.value = { "status": true, "msg": "Company Approved Successfully!" };
            fetchdata();
        } else {
            toast.value = { "status": true, "msg": "Failed to approve the company." };
        }
    } catch (error) {
        toast.value = { "status": true, "msg": "Internal Server Error. Please try again later." };
    }
    finally {
        isloading.value = false;
    }
}

const handleBlock = async (companyId) => {
    const confirmed = confirm("Are You Sure You Want to Block this Company?");
    if (!confirmed) return;
    try {
        const response = await apiClient.patch(`/api/admin/reject-company/${companyId}`);

        if (response.data.status === "success") {
            toast.value = { "status": true, "msg": "Company Blocked Successfully!" };
            fetchdata();
        } else {
            toast.value = { "status": true, "msg": "Failed to Block the company. Try Again..." };
        }
    }
    catch (error) {
        toast.value = response.message
    }
    finally {
        isloading = false;
    }
}

onMounted(() => {
    fetchdata();
});


</script>

<template>
    <AdminNav />

    <div class="container d-flex flex-column align-items-center py-4">
        <!-- Header Section -->
        <h1 class="mb-4 text-center fw-bold text-primary">Company Management</h1>

        <!-- 1. Centered Equal-Width Button Group Container -->
        <div class="w-100 mb-4" style="max-width: 750px;">
            <div class="d-flex border rounded shadow-sm overflow-hidden bg-white">
                <button @click="handlebtn1" type="button" class="btn w-100 rounded-0 py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'approved', 'btn-light text-secondary': active !== 'approved' }">
                    Companies
                </button>

                <button @click="handlebtn2" type="button"
                    class="btn w-100 rounded-0 border-start border-end py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'pending', 'btn-light text-secondary': active !== 'pending' }">
                    New Applications
                </button>

                <button @click="handlebtn3" type="button" class="btn w-100 rounded-0 border-0 py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'blocked', 'btn-light text-secondary': active !== 'blocked' }">
                    Blocked
                </button>
            </div>
        </div>

        <!-- 2. Main Responsive Table Target Section -->
        <div class="w-100" style="max-width: 750px;">
            <div class="table-responsive shadow-sm rounded border bg-white">

                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th scope="col" class="ps-4">Company Name</th>
                            <th scope="col" class="text-end pe-4">Actions</th>
                        </tr>
                    </thead>

                    <!-- Table View A: Approved Companies List -->
                    <tbody v-if="active === 'approved'">


                        <div v-if="isloading" class="text-center py-5">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <tr v-else-if="approvedCompanies.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No approved companies found.</td>
                        </tr>

                        <tr v-for="company in approvedCompanies" :key="company.id">
                            <td class="fw-semibold text-secondary ps-4">{{ company.name }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex gap-3 align-items-center">
                                    <router-link :to="`/admin/company/${company.id}`">
                                        <i class="fa-xl fa-solid fa-eye" title="View Profile"></i>
                                    </router-link>
                                    <i @click="handleBlock(company.id)" class="fa-xl fa-solid fa-ban text-danger"
                                        title="block"></i>
                                </div>
                            </td>
                        </tr>
                    </tbody>


                    <!-- Table View B: Pending Approvals List -->
                    <tbody v-else-if="active === 'pending'">
                        <tr v-if="pendingCompanies.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No pending applications.</td>
                        </tr>
                        <tr v-for="company in pendingCompanies" :key="company.id">
                            <td class="fw-semibold text-secondary ps-4">{{ company.name }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex align-items-center gap-3">

                                    <router-link :to="`/admin/company/${company.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-primary cursor-pointer"
                                            title="Review Details"></i> </router-link>

                                    <i @click="handleApprove(company.id)"
                                        class="fa-xl fa-solid fa-circle-check text-warning cursor-pointer"
                                        title="Approve Company"></i>
                                        <i @click="handleBlock(company.id)" class="fa-xl fa-solid fa-ban text-danger"
                                        title="block"></i>
                                </div>
                            </td>
                        </tr>
                    </tbody>


                    <!-- Table View C: Blocked Companies List -->
                    <tbody v-else-if="active === 'blocked'">
                        <tr v-if="blockedCompanies.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No blocked companies.</td>
                        </tr>
                        <tr v-for="company in blockedCompanies" :key="company.id">
                            <td class="fw-semibold text-secondary ps-4">{{ company.name }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex text-danger">
                                    <router-link :to="`/admin/company/${company.id}`">
                                        <i class="fa-xl fa-solid fa-eye cursor-pointer" title="View Audit Trail"></i>
                                    </router-link>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>


    <div v-if="toast.status" id="loading-toast" class="toast">
        <span> {{ toast.msg }}</span>
        <button @click="toast.status = false" id="close-toast-btn" class="close-btn"
            aria-label="Close message">&times;</button>
    </div>


</template>

<style scoped>
.active-btn {
    background-color: darkgrey;
}


/* Style the close button */
.close-btn {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    font-size: 22px;
    font-weight: bold;
    cursor: pointer;
    line-height: 1;
    padding: 4px;
    transition: color 0.2s ease;
}

i {
    cursor: pointer;
}


.toast {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    /* Ensure it stays on top of everything */

    /* Styling */
    display: flex;
    align-items: center;
    gap: 12px;
    background-color: rgba(33, 33, 33, 0.9);
    color: #ffffff;
    padding: 16px 24px;
    border-radius: 8px;
    font-family: sans-serif;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Simple CSS Loading Spinner */
.spinner {
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>