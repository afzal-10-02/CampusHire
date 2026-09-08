<script setup>
import { ref } from 'vue';
import apiClient from '@/api';

const isStudent = ref(true);
const alertmsg = ref("");
const isloading = ref(false)

const password = ref("");
const confirmpassword = ref("");

const studentdata = ref({
    "email": '',
    "fullname": '',
    "password": '',
    'rollno' : '',
    'branch' : '',
    'cgpa' : '',
    'graduationyear' : '',
    'role' : 'student'
})

const companydata = ref({
    "email": "",
    "companyName": "",
    "password": "",
    "role" : "company",
    "hr_name" : "",
    "hr_phone_no"  : "", 
    "hr_email" : ""
})


const validateData = () => {
    if (isStudent.value) {
        studentdata.value.password = password.value;
    } else {
        companydata.value.password = password.value;
    }

    if (isStudent.value && (!studentdata.value.email || !studentdata.value.fullname || !studentdata.value.rollno || !studentdata.value.branch || !studentdata.value.cgpa || !studentdata.value.graduationyear)) {
        alertmsg.value = "Please the fields."
        return false
    }

    else if (!isStudent.value && (!companydata.value.email || !companydata.value.companyName || !companydata.value.password)) {
        alertmsg.value = "Please all the fields."
        return false
    }

    if (!isStudent?.value) {
    const phone = companydata?.value?.hr_phone_no;

    if (typeof phone !== 'string' || phone.trim().length !== 10) {
        return false;
    }
}

    if (password.value !== confirmpassword.value) {
        alertmsg.value = "Enter Same Password in both fields.";
        return false;
    }
    return true;

}

const handleSubmit = async () => {
    if (isStudent.value){
        studentReg()
    }
    else{
        companyReg()
    }
}

const companyReg = async () => {
    companydata.value.password = password.value;
    const data = companydata.value;

    try {
        isloading.value = true;
        const response = await apiClient.post('/api/company/registration', data);
        alertmsg.value = response.data.message || "Signup successful!";
    } catch (error) {
        console.error(error);
        alertmsg.value = error.response.data.message || "An error occurred during signup.";
    } finally {
        isloading.value = false;
        
    }

}


const studentReg = async () => {
    if(!validateData()){
        alert("hello")
    }

    const data = isStudent.value ? studentdata.value : companydata.value;

    try {
        isloading.value = true;
        const response = await apiClient.post('/api/user/registration', data);
        alertmsg.value = response.data.message || "Signup successful!";
    } catch (error) {
        console.error(error);
        alertmsg.value = error.response.data.message || "An error occurred during signup.";
    } finally {
        isloading.value = false;
        
    }

}

</script>

<template>

    <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
        <form @submit.prevent="handleSubmit" class="border p-4 rounded shadow bg-white">

            <div class="text-center mb-4">
                <h2 class="text-dark">Welcome to CampusHire</h2>
                <h4 class="text-secondary">Registration Form</h4>
            </div>

            <div class="text-center mb-2">
                <input type="radio" name="student" id="student" :value="true" v-model="isStudent" />
                <label for="student">Student</label>

                <input type="radio" name="company" id="company" :value="false" v-model="isStudent" />
                <label for="company">Company</label>

            </div>
            <div v-if="isStudent" class="mb-2 d-flex flex-row gap-2">

                <div>

                    <label for="rollno" class="form-label">Roll No : </label>
                    <input type="text" class="form-control p-2" name="rollno" id="rollno" placeholder="Enter Roll No"
                        v-model="studentdata.rollno" required>

                </div>

                <div>
                    <label for="fullname" class="form-label">Full Name : </label>
                    <input type="text" class="form-control p-2" name="fullname" id="fullname"
                        placeholder="Enter Full Name" v-model="studentdata.fullname" required>
                </div>
            </div>

            <!-- email -->
            <div v-if="isStudent" class="mb-2">
                <label for="username" class="form-label">Student Email : </label>
                <input type="email" class="form-control p-2" name="username" id="username"
                    placeholder="Enter Student Email" v-model="studentdata.email" required>
            </div>
            <div v-else class="mb-2">
                <label for="username" class="form-label">Company Email : </label>
                <input type="email" class="form-control p-2" name="username" id="username"
                    placeholder="Enter Company Email" v-model="companydata.email" required>
            </div>

            <!-- name  -->

            <div v-if="!isStudent" class="mb-2">
                <label for="fullname" class="form-label">Company Name : </label>
                <input type="text" class="form-control p-2" name="fullname" id="fullname"
                    placeholder="Enter Company Name" v-model="companydata.companyName" required>
            </div>

            <!-- Branch -->
            <div v-if="isStudent" class="mb-2 d-flex flex-row gap-2">
                <div>

                    <label for="branch" class="form-label">Branch : </label>
                    <input type="text" class="form-control p-2" name="branch" id="branch" placeholder="Enter Branch"
                        v-model="studentdata.branch" required>

                </div>

                <div>

                    <label for="cgpa" class="form-label">CGPA : </label>
                    <input type="text" class="form-control p-2" name="cgpa" id="cgpa" placeholder="Enter CGPA"
                        v-model="studentdata.cgpa" required>

                </div>
            </div>

            <div v-else class="mb-2 d-flex flex-row gap-2">
                <div>

                    <label for="hr_name" class="form-label">Hr Name : </label>
                    <input type="text" class="form-control p-2" name="hr_name" id="hr_name" placeholder="Hr Name"
                        v-model="companydata.hr_name" required>

                </div>

                <div>

                    <label for="hr_phone_no" class="form-label">Phone No.: </label>
                    <input type="text" class="form-control p-2" name="hr_phone_no" id="hr_phone_no" placeholder="Enter Phone Number"
                        v-model="companydata.hr_phone_no" required>

                </div>
            </div>




            <div v-if="isStudent" class="mb-2">

                <label for="graduationyear" class="form-label">Graduation Year : </label>
                <input type="text" class="form-control p-2" name="graduationyear" id="graduationyear"
                    placeholder="Enter Graduation Year" v-model="studentdata.graduationyear" required>

            </div>

            
            <div v-else class="mb-2">

                <label for="hr_email" class="form-label">Hr Email : </label>
                <input type="text" class="form-control p-2" name="hr_email" id="hr_email"
                    placeholder="Enter Hr Email Id" v-model="companydata.hr_email" required>
            </div>

            <!-- password  -->
            <div class="mb-2 d-flex flex-row gap-2">
                <div>
                    <label for="password" class="form-label">Password : </label>
                    <input type="password" class="form-control p-2" name="password" id="password" v-model="password"
                        placeholder="Enter Password" required>
                </div>

                <div>
                    <label for="confirmpassword" class="form-label">Confirm Password : </label>
                    <input type="password" class="form-control p-2" name="confirmpassword" id="confirmpassword"
                        v-model="confirmpassword" placeholder="Enter Password Again" required>
                </div>
            </div>




            <div v-if="alertmsg" class="alertmsg">
                <small class="alertmsg mx-1 text-danger">{{ alertmsg }}</small>
            </div>

            <p class="mt-3 text-center">
                Already have an account? <a href="/login" class="text-primary">Login here</a>
            </p>
            <button type="submit"
                class="btn btn-primary w-100 d-flex justify-content-center align-items-center" :disabled="isloading">
                <span v-if="isloading" class="spinner-border spinner-border-sm me-2" role="status"
                    aria-hidden="true"></span>
                <span>{{ isloading ? 'Signing up...' : 'Signup' }}</span>
            </button>

        </form>

    </div>

</template>



<style scoped>
.isStudent {
    margin-right: 1rem;
}

.alertmsg {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>