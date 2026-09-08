<script setup>
import apiClient from '@/api';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const isadmin = ref(false)
const svalue = ref("")
const showresult = ref(false)
const results = ref({})
const url = ref("")



onMounted(() => {
    isadmin.value = localStorage.getItem("role") === "admin";
})


const handleSearch = async () => {
    try {
        const response = await apiClient.get(`/api/user/search?q=${svalue.value}`)
        console.log(response.data.data)
        if (response.data.status == "success") {
            showresult.value = true
            results.value = response.data.data
            if (response.data.role == "admin"){
                url.value = "/admin"
            }
            else if(response.data.role == "student") {
                url.value = "/user"
            }
            console.log(response.data.data)
            svalue.value = ""
        }
        else {
            alert("Something Went Wrong, Try Again")

        }
    }
    catch {
        alert("Something Went Wrong, Try Again..")
    }

}



const logout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("role")
    router.push('/login')
}

</script>

<template>
    <nav class="navbar navbar-light bg-dark">
        <a class="navbar-brand" href="#">CampusHire <span v-if="isadmin">Admin</span></a>


        <form @submit.prevent="handleSearch" class="form-inline">
            <input v-model="svalue" class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
            <button type="submit" class="btn btn-outline-success my-2 my-sm-0 btn-search">Search</button>
            <button @click="logout" class="btn btn-outline-danger my-2 my-sm-0 ml-2" type="button">Logout</button>

        </form>




    </nav>

    <div v-if="showresult"
        class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
        style="background: rgba(0,0,0,0.35); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); z-index: 1050;"
        @click.self="showresult = false">

        <div class="bg-white rounded-3 shadow p-4"
            style="width: 90%; max-width: 500px; max-height: 70vh; overflow-y: auto;">

            <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
                <h5 class="mb-0">Search Results</h5>
                <button type="button" class="btn-close" @click="showresult = false" aria-label="Close"></button>
            </div>

            <div>
                <div v-if="results.companies?.length" class="mb-3">
                    <h6 class="text-muted">Companies</h6>
                    <ul class="list-group">
                        <li v-for="c in results.companies" :key="c.id"
                            class="list-group-item d-flex justify-content-between align-items-center">
                            {{ c.name }}
                            <router-link :to="`${url}/company/${c.id}`">
                                <i @click="showresult=false" class="fa-lg fa-solid fa-eye" title="View Profile"></i>
                            </router-link>
                        </li>
                    </ul>
                </div>

                <div v-if="results.drives?.length" class="mb-3">
                    <h6 class="text-muted">Placement Drives</h6>
                    <ul class="list-group">
                        <li v-for="d in results.drives" :key="d.id"
                            class="list-group-item d-flex justify-content-between align-items-center">
                            {{ d.job_title }}
                            <router-link :to="`${url}/drive/${d.id}`">
                                <i @click="showresult=false" class="fa-lg fa-solid fa-eye" title="View Profile"></i>
                            </router-link>
                        </li>
                    </ul>
                </div>




                <div v-if="results.students?.length" class="mb-3">
                    <h6 class="text-muted">Students</h6>
                    <ul class="list-group">
                        <li v-for="s in results.students" :key="s.id"
                            class="list-group-item d-flex justify-content-between align-items-center">
                            {{ s.name }}
                            <router-link :to="`${url}/student/${s.id}`">
                                <i @click="showresult=false" class="fa-lg fa-solid fa-eye" title="View Profile"></i>
                            </router-link>
                        </li>
                    </ul>
                </div>



                <p v-if="!results.companies?.length && !results.drives?.length && !results.students?.length"
                    class="text-muted mb-0">
                    No results found.
                </p>
            </div>
        </div>
    </div>


</template>


<style scoped>
.navbar-brand {
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
    padding-left: 1rem;
}

.form-inline {
    display: flex;
    align-items: center;
    padding-right: 1rem;
}

.form-control {
    margin-right: 0.5rem;
}

.btn-search {
    margin-right: 0.5rem;
}
</style>