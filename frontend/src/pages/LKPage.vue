<template>
    <div class="LK-page">
        <VHeader :title="'личный кабинет'" :toLink="'/'"></VHeader>
        <div class="LK-page__content">
            <div class="user-info">
                <span class="user-info__name">{{ user.name }}</span>
                <span><b>Адрес:</b> {{ user.address }}</span>
                <span><b>Номер телефона:</b> {{ user.phone }}</span>
                <span><b>Почта:</b> {{ user.email }}</span>
            </div>
            <h2 class="user-orders__title">мои заказы</h2>
            <table>
                <thead>
                    <tr>
                    <th>Номер</th>
                    <th>Состав</th>
                    <th>Сумма</th>
                    <th>Статус</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(order, index) in orders" :key="index">
                    <td>{{ order.id.slice(0, 4) }}</td>
                    <td>
                        {{ ordersPizzas[index].join(', ')}}
                    </td>
                    <td>{{ order.summ }}</td>
                    <td>{{ order.status ? 'доставляется': 'готовится'}}</td>
                    </tr>
                </tbody>
            </table>
            <div class="LK-page__actions">
                <VButtonWhite :title="'выйти'" class="LK-button" :click="'exit'" @exit="exitModal"></VButtonWhite>
                <RouterLink to="/edit_info" class="LK-page__link">
                    <VButtonRed :title="'редактировать'" class="LK-edit-button"></VButtonRed>
                </RouterLink>
            </div>
        </div>
        <VExitModal
            :isVisible="isModalVisible"
            :title="modalTitle"
            @close="closeModal"
        ></VExitModal>
    </div>
</template>

<script>
import VHeader from '../components/VHeader.vue';
import VButtonWhite from '../components/VButtonWhite.vue';
import VButtonRed from '../components/VButtonRed.vue';
import VExitModal from '../components/VExitModal.vue';

import axios from 'axios';

export default {
    name: 'LKPage',
    components: {
        VButtonRed,
        VHeader,
        VButtonWhite,
        VExitModal,
    },
    data(){
        return {
            user: [],
            error: null,
            orders: [],
            ordersPizzas: [],
            isModalVisible: false,
            modalTitle: null,
        };
    },
    methods: {
        async getUser() {
            try {
                const response = await axios.get('http://localhost:8001/users/get_user?email=user%40example.com'); // Замените на ваш URL
                this.user = response.data.data;
                this.getUserOrders();
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        },
        async getUserOrders() {
            try {
                const response = await axios.get('http://localhost:8001/users/get_user_orders?email=user%40example.com'); // Замените на ваш URL
                this.orders = response.data.data;
                const ordersId = this.orders.map(order => order.id);
                console.log(ordersId);
                ordersId.forEach((id) => {
                    this.getOrder(id); 
                });
                
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        },
        async getOrder(id) {
            try {
                console.log(id);
                const response = await axios.get(`http://localhost:8001/admin/get_order_content/${id}`);
                this.ordersPizzas.push(response.data.data.map(el => el.pizza_name));
                this.ordersPizzas.reverse();
                console.log(this.ordersPizzas);
                console.log(7);
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; 
                console.error('Ошибка при получении пицц:', error);
            }
        },
        exitModal(){
            this.modalTitle = 'Вы действительно хотите выйти?';
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },

    },
    created(){
        this.getUser();
    }
}
</script>

<style>
.LK-page{
    color: #CA151C;
    font-family: Nunito;
    overflow-x: hidden;
    width:100%;
    height:100%;
}
.LK-page__content{
    margin: 0 90px;
}
.user-info{
    display:flex;
    flex-direction: column;
    margin: 10px 0;
    font-size: 1.7rem;
    justify-content:space-around;
    height: 30%;
    font-weight: 300;
}
.user-info__name{
    font-weight: 800;
    font-size: 2.3rem;
}
.user-orders__title{
    margin: 10px 0;
    font-weight: 800;
    font-size: 2.5rem;
}
table {
    font-size: 1.5rem;
    width: 100%;
    border-collapse: separate;
    border-spacing: 2px;
    /* border-radius: 20px;  */
    overflow: hidden;
    /* border: 3px solid #BF0200; */
}
td div {
    margin: 5px 0;
}
th, td {
    border: 3px solid #BF0200;
    padding: 8px; 
    text-align: left;
    border-radius: 17px; 
}
th {
    background-color: #FFE9C1;
    font-weight: bold; 
}
.LK-page__actions{
    display: flex;
    justify-content: space-between;
    /* margin: 100px 0 30px 0; */
    margin: 60px 0 20px 0;
    width: 100%;
}
.LK-button, .LK-page__link{
    width: 40%;
}
.LK-edit-button{
    width: 100%;
}
</style>
