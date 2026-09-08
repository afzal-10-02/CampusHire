<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import StudentNav from '@/components/StudentNav.vue';

const historyData = ref([])
const history = ref([]);
const isloading = ref(false);
const selectedFilter = ref("all")

const getStatusBadge = (status) => {
    if (status === 'Selected') return 'bg-success';
    if (status === 'Rejected') return 'bg-danger';
    if (status === 'Shortlisted') return 'bg-primary';
    return 'bg-warning text-dark';
};

const filterDrive = (status) => {
    selectedFilter.value = status
    if (status == "all") {
        history.value = historyData.value;
    }
    else if (status == "Applied") {
        history.value = historyData.value.filter(item => {
            const itemStatus = ("pending" || '').toLowerCase();
            return itemStatus === status;
        });

    }
    else {
        history.value = historyData.value.filter(item => {
            const itemStatus = (item.status || '').toLowerCase();
            return itemStatus === status;
        });
    }

}

const getHistory = async () => {
    isloading.value = true;
    try {
        const response = await apiClient.get('/api/user/get-history');
        if (response.data.status === 'success') {
            console.log(response.data.data)
            historyData.value = response.data.data;
            filterDrive('all')
        }
        else {
            alert(response.data.message)
        }
    } catch (error) {
        if (error.response) {
            alert(error.response.data.message)
        }
        console.error('Error fetching application history:', error);
    } finally {
        isloading.value = false;
    }
};

const exportData = async () => {
    try {
        const response = await apiClient.get('/api/user/export-placement-records')
        if (response.data.status == "success") {
            alert(response.data.message)
        }
        else {
            alert("Internal Server Error, Try Again...")

        }

    } catch (error) {
        alert("Internal Server Error, Try Again...")

    }
}

onMounted(() => {
    getHistory();
});
</script>

<template>
    <StudentNav />


    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center w-100">
            <div class="dropdown mb-1">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">
                    Filter By: {{ selectedFilter }}
                </button>

                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" @click.prevent="filterDrive('all')">All</a></li>
                    <li><a class="dropdown-item" href="#" @click.prevent="filterDrive('Applied')">Applied</a></li>
                    <li><a class="dropdown-item" href="#" @click.prevent="filterDrive('Shortlisted')">Shorlisted</a>
                    </li>
                    <li><a class="dropdown-item" href="#" @click.prevent="filterDrive('Rejected')">Rejected</a></li>
                </ul>
            </div>
            <div>

                <button @click="exportData" class="btn btn-primary ms-5">Export Placement Data</button>
            </div>
        </div>

        <div class="border rounded shadow-sm bg-white">
            <div class="border-bottom p-3 bg-light">
                <span class="fw-semibold fs-6">Application History</span>
            </div>

            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th scope="col" class="ps-4">Job Title</th>
                            <th scope="col">Company</th>
                            <th scope="col">Applied On</th>
                            <th scope="col">Remarks</th>
                            <th scope="col" class="text-end pe-4">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="isloading">
                            <td colspan="5" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </td>
                        </tr>

                        <tr v-else-if="history.length === 0">
                            <td colspan="5" class="text-center text-muted py-4">No applications yet.</td>
                        </tr>

                        <tr v-for="item in history" :key="item.application_id" v-else>
                            <td class="fw-semibold text-secondary ps-4">{{ item.job_title }}</td>
                            <td class="text-secondary">{{ item.company_name }}</td>
                            <td class="text-secondary">{{ item.application_date }}</td>
                            <td class="text-secondary">{{ item.remarks || '—' }}</td>
                            <td class="text-end pe-4">
                                <span class="badge px-3 py-2" :class="getStatusBadge(item.status)">
                                    {{ item.status }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<style scoped></style>