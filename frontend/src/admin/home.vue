<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api'
import AdminNav from '@/components/AdminNav.vue'

const isLoading = ref(true)
const errorMsg = ref("")

const data = ref({
    "students": {
        "total": 0,
        "blocked": 0,
        "active": ""
    },
    "drives": {
        "total": 0,
        "active": 0,
        "rejected": 0,
        "pending": 0,
        "completed": 0
    },
    "companies": {
        "total": 0,
        "active": 0,
        "pending": 0,
        "rejected": 0
    }
})

const getdata = async () => {
    try {
        const response = await apiClient.get('/api/admin/get-overview')
        if (response.status === 200) {
            data.value = response.data.data
        }
    } catch (error) {
        console.error("Failed to load metrics:", error)
        errorMsg.value = "Failed to synchronize live statistics."

    } finally {
        isLoading.value = false
    }
}

onMounted(() =>
    getdata()
)


</script>

<template>
    <AdminNav />


    <!-- Main Container -->
    <div class="container-fluid py-4 px-4">

        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="text-dark fw-bold mb-0">System Overview</h3>
            <span v-if="isLoading" class="spinner-border spinner-border-sm text-secondary" role="status"></span>
        </div>

        <div v-if="errorMsg" class="alert alert-warning py-1 small mb-4" role="alert">
            {{ errorMsg }} (Using offline data preview)
        </div>

        <!-- Main 3-Column Container -->
        <div class="row g-4">

            <!-- COLUMN 1: Student Insights -->
            <div class="col-12 col-md-4">
                <div class="card h-100 border-dark border-2 p-4 bg-white text-center">
                    <h5 class="text-dark fw-bold mb-4 text-start border-bottom pb-2">Student Insights</h5>

                    <!-- Row 1: Two blocks side-by-side -->
                    <div class="row g-3 mb-3">
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Total Enrolled</div>
                                <div class="fs-4 fw-bold text-dark">{{ data.students.total }}</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Active</div>
                                <div class="fs-4 fw-bold text-success">{{ data.students.active }}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Row 2: Centered single block at the bottom -->
                    <div class="row justify-content-center">
                        <div class="col-8">
                            <div class="border border-dark p-3 rounded bg-light">
                                <div class="text-secondary small fw-medium mb-1">Blocked</div>
                                <div class="fs-4 fw-bold text-danger">{{ data.students.blocked }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- COLUMN 2: Hiring Campaigns -->
            <div class="col-12 col-md-4">
                <div class="card h-100 border-dark border-2 p-4 bg-white text-center">
                    <h5 class="text-dark fw-bold mb-4 text-start border-bottom pb-2">Drives Insights</h5>

                    <!-- Row 1: Two blocks side-by-side -->
                    <div class="row g-3 mb-3">
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Total Campaigns</div>
                                <div class="fs-4 fw-bold text-dark">{{ data.drives.total }}</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Active</div>
                                <div class="fs-4 fw-bold text-primary">{{ data.drives.active }}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Row 2: Two blocks side-by-side -->
                    <div class="row g-3 mb-3">
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Completed</div>
                                <div class="fs-4 fw-bold text-success">{{ data.drives.completed }}</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Blocked</div>
                                <div class="fs-4 fw-bold text-danger">{{ data.drives.rejected }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="row justify-content-center">
                        <div class="col-8">
                            <div class="border border-dark p-3 rounded bg-light">
                                <div class="text-secondary small fw-medium mb-1">Pendig Drives</div>
                                <div class="fs-4 fw-bold text-danger">{{ data.drives.pending }}</div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- COLUMN 3: Corporate Ecosystem -->
            <div class="col-12 col-md-4">
                <div class="card h-100 border-dark border-2 p-4 bg-white text-center">
                    <h5 class="text-dark fw-bold mb-4 text-start border-bottom pb-2">Company Insights</h5>

                    <!-- Row 1: Two blocks side-by-side -->
                    <div class="row g-3 mb-3">
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">Total Companies</div>
                                <div class="fs-4 fw-bold text-dark">{{ data.companies.total }}</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="border border-dark p-3 rounded h-100 bg-light">
                                <div class="text-secondary small fw-medium mb-1">New Apps</div>
                                <div class="fs-4 fw-bold text-warning">{{ data.companies.pending }}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Row 2: Centered single block at the bottom -->
                    <div class="row justify-content-center">
                        <div class="col-8">
                            <div class="border border-dark p-3 rounded bg-light">
                                <div class="text-secondary small fw-medium mb-1">Blocked</div>
                                <div class="fs-4 fw-bold text-muted">{{ data.companies.rejected }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<style scoped>
.card {
    border-radius: 4px !important;
}
</style>
