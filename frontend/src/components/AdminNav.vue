<script setup>

</script>
<template>
    <div class="d-flex flex-wrap justify-content-center gap-3 bg-light p-3 rounded shadow-sm">
        <router-link to="/admin" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
            Dashboard
        </router-link>

        <router-link to="/admin/companies" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
            Companies
        </router-link>

        <router-link to="/admin/students" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
            Students
        </router-link>

        <router-link to="/admin/drives" class="btn btn-outline-primary px-4 rounded-pill fw-semibold">
            Placement Drives
        </router-link>
    </div>


</template>
