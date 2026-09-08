<script setup>
import AdminNav from '@/components/AdminNav.vue';
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import ViewDrive from '@/components/ViewDrive.vue';


const props = defineProps({
    isChild: Boolean,
    companyId: Number,
    isCompanyView: {
        type: Boolean,
        default: false
    }
})



const active = ref("approved")
const isviewDrive = ref(false)
const viewDriveId = ref()
const preurl = ref('/admin')

const handlebtn1 = () => active.value = "approved";
const handlebtn2 = () => active.value = 'pending';
const handlebtn3 = () => active.value = "blocked";
const handlebtn4 = () => active.value = 'completed';




const approvedDrives = ref([])
const pendingDrives = ref([])
const blockedDrives = ref([])
const completedDrives = ref([])


const viewDrive = (id) => {
    isviewDrive.value = true
    viewDriveId.value = id
}



const approveDrive = async (id) => {
    confirm("Approve Drive, Are You Sure?")
    try {
        const response = await apiClient.put(`/api/admin/approve-drive/${id}`)
        if (response.data.status == "success") {
            alert(response.data.message)
            getdrives()
        }
        else {
            alert(response.data.message)

        }
    }

    catch (error) {
        alert("Internal Server Error, Try Again...")
    }
}

const blockDrive = async (id) => {
    confirm("Block Drive, Are You Sure?")
    try {
        const response = await apiClient.put(`/api/admin/block-drive/${id}`)
        if (response.data.status == "success") {
            alert(response.data.message)
            getdrives()
        }
        else {
            alert(response.data.message)

        }
    }

    catch (error) {
        alert("Internal Server Error, Try Again...")
    }
}


const getdrives = async (id = null) => {
    let url = ''
    if (id !== null) {
        url = `/api/admin/get-drives/${id}`
    }
    else {
        url = `/api/admin/get-drives`
    }
    try {
        const response = await apiClient.get(url);
        if (response.data.status === "success") {
            approvedDrives.value = response.data.data.approvedDrives;
            pendingDrives.value = response.data.data.pendingDrives;
            blockedDrives.value = response.data.data.rejectedDrives;
            completedDrives.value = response.data.data.completedDrives;

        } else {
            console.error("Failed to fetch student data:", response.data.message)
        }
    } catch (error) {
        console.error("Error fetching student data:", error)
    }
    finally{
        if (props.isCompanyView){
            preurl.value = '/company'
        }else{
            preurl.value = '/admin'
        }
    }
}

onMounted(() => {
    if (props.isChild && props.companyId !== null) {
        getdrives(props.companyId)

    } else {
        getdrives()
    }
})




</script>

<template>
    <AdminNav v-if="!props.isChild" />

    <div class="container d-flex flex-column align-items-center py-4">
        <!-- Header Section -->
        <h1 v-if="props.isChild" class="mb-4 text-center fw-bold text-primary">Drives</h1>
        <h1 v-else class="mb-4 text-center fw-bold text-primary">Drives Management</h1>



        <!-- 1. Centered Equal-Width Button Group Container -->
        <div class="w-100 mb-4" style="max-width: 750px;">
            <div class="d-flex border rounded shadow-sm overflow-hidden bg-white">
                <button @click="handlebtn1" type="button" class="btn w-100 rounded-0 border-0 py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'approved', 'btn-light text-secondary': active !== 'approved' }">
                    Drives
                </button>

                <button @click="handlebtn2" type="button"
                    class="btn w-100 rounded-0 border-0 border-start border-end py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'pending', 'btn-light text-secondary': active !== 'pending' }">
                    New Applications
                </button>

                <button @click="handlebtn3" type="button" class="btn w-100 rounded-0 border-0 py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'blocked', 'btn-light text-secondary': active !== 'blocked' }">
                    Blocked Drives
                </button>

                <button @click="handlebtn4" type="button" class="btn w-100 rounded-0 border-0 py-2 fw-semibold"
                    :class="{ 'active-btn': active === 'completed', 'btn-light text-secondary': active !== 'completed' }">
                    Completed
                </button>


            </div>
        </div>

        <!-- 2. Main Responsive Table Target Section -->
        <div class="w-100" style="max-width: 750px;">
            <div class="table-responsive shadow-sm rounded border bg-white">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th scope="col" class="ps-4">Drive Name</th>
                            <th scope="col" class="ps-4">Company Name</th>

                            <th scope="col" class="text-end pe-4">Actions</th>
                        </tr>
                    </thead>

                    <!-- Table View A: Approved Companies List -->
                    <tbody v-if="active === 'approved'">
                        <tr v-if="approvedDrives?.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No approved Drives found.</td>
                        </tr>
                        <tr v-for="drive in approvedDrives" :key="drive.id">
                            <td class="fw-semibold text-secondary ps-4">{{ drive.name }}</td>
                            <td class="fw-semibold text-secondary ps-4"> {{ drive.companyName }}</td>

                            <td class="text-end pe-4">
                                <div class="d-inline-flex align-items-center gap-3 ">
                                    <router-link :to="`${preurl}/drive/${drive.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-primary" title="View Drive"></i>
                                    </router-link>
                                    <i @click="blockDrive(drive.id)" class="fa-xl fa-solid fa-ban text-danger"
                                        title="block"></i>
                                </div>
                            </td>
                        </tr>
                    </tbody>

                    <!-- Table View B: Pending Approvals List -->
                    <tbody v-else-if="active === 'pending'">
                        <tr v-if="pendingDrives?.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No Pending Drives.</td>
                        </tr>
                        <tr v-for="drive in pendingDrives" :key="drive.id">
                            <td class="fw-semibold text-secondary ps-4">{{ drive.name }}</td>
                            <td class="fw-semibold text-secondary ps-4"> {{ drive.companyName }}</td>

                            <td class="text-end pe-4">
                                <div class="d-inline-flex align-items-center gap-3">
                                    <router-link :to="`${preurl}/drive/${drive.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-danger" title="View Drive"></i>
                                    </router-link>
                                    <i v-if="!props.isCompanyView" @click="approveDrive(drive.id)"
                                        class="fa-xl fa-solid fa-circle-check text-warning cursor-pointer"
                                        title="Approve Drive"></i>
                                    <i v-if="!props.isCompanyView" @click="blockDrive(drive.id)" class="fa-xl fa-solid fa-ban text-danger"
                                        title="block"></i>

                                </div>
                            </td>
                        </tr>
                    </tbody>

                    <!-- Table View C: Blocked Companies List -->
                    <tbody v-else-if="active === 'blocked'">
                        <tr v-if="blockedDrives?.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No blocked Drives.</td>
                        </tr>
                        <tr v-for="drive in blockedDrives" :key="drive.id">
                            <td class="fw-semibold text-secondary ps-4">{{ drive.name }}</td>
                            <td class="fw-semibold text-secondary ps-4"> {{ drive.companyName }}</td>

                            <td class="text-end pe-4">
                                <div class="d-inline-flex text-danger">
                                    <router-link :to="`${preurl}/drive/${drive.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-primary" title="View Drive"></i>
                                    </router-link>
                                </div>
                            </td>
                        </tr>
                    </tbody>

                    <tbody v-else-if="active === 'completed'">
                        <tr v-if="completedDrives?.length === 0">
                            <td colspan="2" class="text-center text-muted py-4">No Completed Drives.</td>
                        </tr>
                        <tr v-for="drive in completedDrives" :key="drive.id">
                            <td class="fw-semibold text-secondary ps-4">{{ drive.name }}</td>
                            <td class="fw-semibold text-secondary ps-4"> {{ drive.companyName }}</td>
                            <td class="text-end pe-4">
                                <div class="d-inline-flex text-danger">
                                    <router-link :to="`${preurl}/drive/${drive.id}`">
                                        <i class="fa-xl fa-solid fa-eye text-danger" title="View Drive"></i>
                                    </router-link>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <ViewDrive v-if="isviewDrive" :id="viewDriveId" @close="isviewDrive = false" />



</template>

<style scoped>
.active-btn {
    background-color: darkgrey;
}


i {
    cursor: pointer;
}
</style>