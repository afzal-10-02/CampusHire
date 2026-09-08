<script setup>
import { onMounted, ref } from 'vue';
import AdminNav from '@/components/AdminNav.vue';
import apiClient from '@/api';

const active = ref("approved")

const handlebtn1 = () => active.value = "approved";
const handlebtn2 = () => active.value = "blocked";



const activeStudents = ref([])


const blockedStudents = ref([])


const blockStudent = async (id) => {
    const con = confirm("Are You Sure You Want to Block this Student...")
    if(!con){
        return
    }
    try {

        const response = await apiClient.put(`/api/admin/block-student/${id}`)
        if (response.status == 200){
            alert("Student Blocked Successfully.")
            getdata()
        }
        else{
            alert(response.data.message)
        }

    }
    catch (error) {
        alert("Internal Server Error, Try Again...")
        console.log(error)
    }
}


const getdata = async () => {
    try {
        const response = await apiClient.get('/api/admin/get-students')
        if (response.status == 200) {
            console.log(response.data.data)
            activeStudents.value = response.data.data.active
            blockedStudents.value = response.data.data.blocked
        }
        else {
            console.log(response.data.data)
        }
    }
    catch (error) {
        alert("Internal Sever Error, Try Again")
    }

}

onMounted(() => {
    getdata()
})




</script>

<template>
    <AdminNav />

    <div class="container d-flex flex-column align-items-center py-4">
        <!-- Header Section -->
        <h1 class="mb-4 text-center fw-bold text-primary">Student Management</h1>

        <!-- 1. Centered Equal-Width Button Group Container -->
        <div class="w-100 mb-4" style="max-width: 750px;">
            <div class="d-flex border rounded shadow-sm overflow-hidden bg-white">
                <button @click="handlebtn1" type="button" class="btn w-100 rounded-0 border-0 py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'approved', 'btn-light text-secondary': active !== 'approved' }">
                    Students
                </button>
                <!-- 
                <button @click="handlebtn2" type="button"
                    class="btn w-100 rounded-0 border-0 border-start border-end py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'pending', 'btn-light text-secondary': active !== 'pending' }">
                    New Applications
                </button> -->

                <button @click="handlebtn2" type="button" class="btn w-100 rounded-0 border-0 py-2 fw-semibold"
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
                            <th scope="col" class="ps-4">Student Name</th>
                            <th scope="col" class="text-end pe-4">Actions</th>
                        </tr>
                    </thead>

                    <!-- Table View A: Approved Companies List -->
                    <tbody v-if="active === 'approved'">
                        <tr v-if="activeStudents.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No approved Students found.</td>
                        </tr>
                        <tr v-for="student in activeStudents" :key="student.id">
                            <td class="fw-semibold text-secondary ps-4">{{ student.full_name }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex  gap-3   align-items-center">
                                    <router-link :to="`/admin/student/${student.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-primary" title="View Profile"></i>

                                    </router-link>
                                    <i @click="blockStudent(student.id)" class="fa-xl fa-solid fa-ban text-danger" title="block"></i>
                                </div>
                            </td>
                        </tr>
                    </tbody>

                    <!-- Table View B: Pending Approvals List
                    <tbody v-else-if="active === 'pending'">
                        <tr v-if="pendingStudents.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No pending Students.</td>
                        </tr>
                        <tr v-for="student in pendingStudents" :key="student.id">
                            <td class="fw-semibold text-secondary ps-4">{{ student.name }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex gap-3">
                                    <i class="fa-xl fa-solid fa-eye text-primary cursor-pointer"
                                        title="Review Details"></i>
                                    <i class="fa-xl fa-solid fa-circle-check text-warning cursor-pointer"
                                        title="Approve Student"></i>
                                </div>
                            </td>
                        </tr>
                    </tbody> -->

                    <!-- Table View C: Blocked Companies List -->
                    <tbody v-else-if="active === 'blocked'">
                        <tr v-if="blockedStudents.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No blocked Students.</td>
                        </tr>
                        <tr v-for="student in blockedStudents" :key="student.id">
                            <td class="fw-semibold text-secondary ps-4">{{ student.full_name }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex text-danger">
                                    <router-link :to="`/admin/student/${student.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-danger" title="View Profile"></i>

                                    </router-link>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>







</template>

<style scoped>
.active-btn {
    background-color: darkgrey;
}


i {
    cursor: pointer;
}
</style>