import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    

    {
        path: "/login",
        name: "login",
        component: () => import('./components/Login.vue'),
         meta: { isPublic: true } 
    },

    {
        path: "/signup",
        name: "signup",
        component: () => import('./components/Signup.vue'),
         meta: { isPublic: true } 
    },

    {
      path: "/company/home",
      name: "companyHome",
      component: () => import('./company/home.vue')
    },
    {
      path : "/company/edit-profile",
      name : "companyeditProfile",
      component : () => import("./company/EditProfile.vue")
    },
  
    {
      path: "/company/drive/:id",
      name: "CompanyDrivePage",
      component : () => import('./company/Drive.vue')
    },
    {
      path: "/company/drives",
      name: "CompanyDrivesPage",
      component : () => import('./company/Drives.vue')
    },

    {
      path: "/admin",
      name : "admin",
      component : () => import('./admin/home.vue')
    },

    {
      path: "/admin/companies",
      name : "adminCompanies",
      component : () => import('./admin/companies.vue')
    }, 

    {
      path: "/admin/students",
      name : "adminStudents",
      component : () => import('./admin/students.vue')
    },

    {
      path: "/admin/drives",
      name : "adminDrives",
      component : () => import('./admin/drives.vue'),
      props: { isChild: false , companyId: null } 

    },
    {
      path: "/admin/drive/:id",
      name : "adminDrive",
      component : () => import('./admin/drive.vue'),
    },

    {
      path :"/admin/company/:id",
      name : "adminCompany",
      component : () =>import("./admin/company.vue"),
    },
    {
      path : "/admin/student/:id",
      name : "adminStudent",
      component : () => import("./admin/student.vue")
    },

    {
      path: "/",
      name: "studentDashboard",
      component : () => import('./user/home.vue')
    },

    {
      path: "/company/usr",
      name: "comapnyPage",
      component : () => import('./user/CompanyPage.vue')
    },

    {
      path: "/user/edit-profile",
      name: "editProfile",
      component : () => import('./user/EditProfile.vue')
    },
    {
      path: "/user/history",
      name: "UserHistory",
      component : () => import('./user/history.vue')
    },
    {
      path: "/user/company/:id",
      name: "UserCompany",
      component : () => import('./user/CompanyPage.vue')
    },
    {
      path: "/user/drive/:id",
      name: "UserDrive",
      component : () => import('./user/drive.vue')
    }
    
  ],
})

router.beforeEach((to, from) => {
  const token = localStorage.getItem('access_token');

  const isProtectedPage = !to.meta.isPublic;

  if (isProtectedPage && !token) {
    console.warn('Unauthorized access attempt. Redirecting to /login');
    next('/login');
  } 

  else if (token && to.meta.isPublic) {
    return '/'
  } 
  
  return true
});

export default router
