<script setup>
import apiClient from '@/api';
import { ref } from 'vue'
import { useRouter } from 'vue-router'; 

const router = useRouter(); 

const email = ref("")
const password = ref("")
const role = ref("student")
const msg = ref("")
const isLoading = ref(false)


const handleLogin = async () => {
    isLoading.value = true
    msg.value = ""
    const payload = {
        email: email.value,
        password: password.value,
        role: role.value
    }
    try {
        const response = await apiClient.post("/api/auth/login", payload)


        if (response.status === 200) {
            localStorage.setItem("access_token", response.data.access_token)
            localStorage.setItem("role", response.data.role)
            localStorage.setItem("name", response.data.name)
            if (response.data.role === "student") {
                router.push('/')
            } else if (response.data.role === "company") {
                router.push('/company/home')
            } else if (response.data.role === "admin") {
                router.push('/admin')
            }
            else {
                msg.value = response.data.message;
            }
        }
        else {
            msg.value = response.data.message
        }

    }
    catch (error) {
         msg.value = error.response?.data?.message
    }
    finally {
        isLoading.value = false
    }
}


</script>


<template>

    <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
        <form @submit.prevent="handleLogin" class="border p-4 rounded shadow bg-white" method="POST">
            <div class="text-center mb-4">
                <h2 class="text-dark">Welcome to CampusHire</h2>
                <h4 class="text-secondary">Login</h4>
            </div>

            <!-- Role Selection Radio Buttons -->
            <div class="mb-2 text-center">
                <div class="btn-group w-100" role="group">
                    <input type="radio" class="btn-check" name="role" id="roleStudent" value="student" v-model="role"
                        checked>
                    <label class="btn btn-outline-primary" for="roleStudent">Student</label>

                    <input type="radio" class="btn-check" name="role" id="roleCompany" value="company" v-model="role">
                    <label class="btn btn-outline-primary" for="roleCompany">Company</label>

                    <input type="radio" class="btn-check" name="role" id="roleAdmin" value="admin" v-model="role">
                    <label class="btn btn-outline-primary" for="roleAdmin">Admin</label>
                </div>
            </div>

            <div class="mb-3">
                <label for="username" class="form-label">Email : </label>
                <input type="email" class="form-control p-2" name="username" id="username" placeholder="Enter email"
                    v-model="email" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password : </label>
                <input type="password" class="form-control p-2" name="password" id="password" placeholder="Password"
                    v-model="password" required>
            </div>

            <small v-if="msg" class="text-danger">{{ msg }}</small>


            <p class="mt-3 text-center">
                Don't have an account? <a href="/signup" class="text-primary">Register here</a>
            </p>

            <button class="btn btn-primary w-100">
                
                <span v-if="isLoading">
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Logging in...
                </span>

                <span v-else>
                    Login
                </span>
            </button>
        </form>
    </div>


</template>



<style></style>