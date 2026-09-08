<script setup>
import { ref } from 'vue';
import CreateDrive from '@/components/CreateDrive.vue';
import StudentNav from '@/components/StudentNav.vue';
import Drives from '@/admin/drives.vue';

const isCreateDrive = ref(false);



</script>

<template>
    <StudentNav iscompany=true />

    <div class="container d-flex flex-column align-items-center min-vh-100 py-4">
        <div class="w-100" style="max-width: 750px;">

            <Drives :isChild ="true" :is-company-view="true"/>
            

            <div class="text-center">
                <button @click="isCreateDrive = true"
                    class="btn btn-primary px-4 py-2 rounded-pill fw-semibold shadow-sm">
                    <i class="fa-solid fa-plus me-2"></i>Create New Drive
                </button>
            </div>
        </div>

        <CreateDrive v-if="isCreateDrive" @cancel="isCreateDrive = false" />
    </div>
</template>

<style scoped>
.active {
    background-color: darkgrey;
}

i {
    cursor: pointer;
}
</style>