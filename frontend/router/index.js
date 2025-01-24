import Vue from 'vue';
import VueRouter from 'vue-router';
import BasketPage from '../src/pages/BasketPage.vue';
import HomePage from '../src/pages/HomePage.vue';
import LKPage from '../src/pages/LKPage.vue';
import SendOrderPage from '../src/pages/SendOrderPage.vue';
import EditUserInfoPage from '../src/pages/EditUserInfoPage.vue';

const routes = [
  {
    path: '/basket',
    name: 'BasketPage',
    component: BasketPage
  },
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/LK',
    name: 'LKPage',
    component: LKPage,
  },
  {
    path: '/send_order',
    name: 'SendOrderPage',
    component: SendOrderPage,
  },
  {
    path: '/edit_info',
    name: 'EditUserInfoPage',
    component: EditUserInfoPage,
  },
];


Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'history',
    routes,
});

export const redirect = (path) => {
    router.push(path);
};

export default router;
