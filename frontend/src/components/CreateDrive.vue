<script setup>
import { ref } from 'vue';
import apiClient from '@/api';

defineEmits(['cancel'])

const form = ref({
    company_id: 2,
    job_title: '',
    job_description: '',
    eligible_branches: '',
    min_cgpa: null,
    eligible_year: null,
    application_deadline: ''
});


const handleSubmit = async () => {
    const payload = form.value;

    try {
        const response = await apiClient.post('/api/company/create-drive', payload);
        
        if (response.status == 200) {
            alert(response.data.message);
        } else {
            alert(response.data.message || "Something Went Wrong, Try Again..");
        }
        
    } catch (error) {
        if (error.response){
            alert(error.response.data?.message);
        }
        else{
       alert("Internal Server Error, try Again...")
    }}
};

</script>


<template>
    <div class="div-one">
        <div class="div-two">
            <h2 class="form-title">CREATE NEW PLACEMENT DRIVE</h2>

            <form @submit.prevent="handleSubmit">

                <div class="mb-3">
                    <label for="job_title" class="form-label">Job Title</label>
                    <input type="text" id="job_title" v-model="form.job_title" class="form-control"
                        placeholder="e.g., Software Engineer Intern" required />
                </div>

                <div class="mb-3">
                    <label for="job_description" class="form-label">Job Description</label>
                    <textarea id="job_description" v-model="form.job_description" class="form-control" rows="3"
                        placeholder="Role responsibilities, skills required, etc..." required></textarea>
                </div>


                <div class="row g-3 mb-3">
                    <div class="col-md-8">
                        <label for="eligible_branches" class="form-label">Eligible Branches</label>
                        <input type="text" id="eligible_branches" v-model="form.eligible_branches" class="form-control"
                            placeholder="e.g., CSE, IT, ECE" required />
                    </div>
                    <div class="col-md-4">
                        <label for="min_cgpa" class="form-label">Min CGPA</label>
                        <input type="number" step="0.01" min="0" max="10" id="min_cgpa" v-model="form.min_cgpa"
                            class="form-control" placeholder="0.00" required />
                    </div>
                </div>

                <div class="row g-3 mb-4">
                    <div class="col-md-5">
                        <label for="eligible_year" class="form-label">Passing Year</label>
                        <input type="number" id="eligible_year" v-model="form.eligible_year" class="form-control"
                            placeholder="e.g., 2026" required />
                    </div>
                    <div class="col-md-7">
                        <label for="application_deadline" class="form-label">Application Deadline</label>
                        <input type="datetime-local" id="application_deadline" v-model="form.application_deadline"
                            class="form-control" required />
                    </div>
                </div>

                <div class="d-flex justify-content-end gap-2 mt-4">
                    <button type="submit" class="btn btn-primary px-4">
                        Submit Drive
                    </button>
                    <button type="button" class="btn btn-outline-secondary px-4" @click="$emit('cancel')">
                        Cancel
                    </button>
                </div>

            </form>
        </div>
    </div>
</template>



<style scoped>
/* Centered popup backdrop overlay */
.div-one {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
    padding: 20px;
}

/* Square Card Box styling */
.div-two {
    background: #ffffff;
    width: 100%;
    max-width: 600px;
    aspect-ratio: 1 / 1;
    padding: 40px;
    border-radius: 5px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow-y: auto;
}

.form-title {
    font-weight: 700;
    letter-spacing: 0.5px;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 10px;
}

/* Sharp inputs to match the square theme */
.form-control {
    border-radius: 0px !important;
    border: 1px solid #cbd5e1;
}

.form-control:focus {
    border-color: #3b82f6;
    box-shadow: none;
}
</style>