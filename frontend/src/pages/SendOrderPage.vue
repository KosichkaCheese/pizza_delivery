<template>
    <div class="sendOrder-page">
        <VHeader :title="'ваш заказ'" :toLink="'/basket'"></VHeader>
        <template>
            <VPizzaBasketCard
                v-for="(position, index) in order" 
                :key="index" 
                :name="position.pizza_name" 
                :cost="position.pizza_cost"
                :amount="position.count"
            ></VPizzaBasketCard>
        </template>
        <div class="sendOrder-page__actions">
            <!-- <VButtonWhite :title="'очистить корзину'"></VButtonWhite> -->
            <span class="sendOrder-page__sum">итого: {{ orderSumm}} руб.</span>
        </div>
        <div class="sendOrder__user-info">
                <span><b>Получатель: </b>{{ user.name }}</span>
                <div class="user-info__input">
                    <span class="order-input__label"><b>Адрес:</b></span><input class="order-input" v-model="userAddress" :disabled="isDisabled" required>
                </div>
                <div class="user-info__input">
                    <span class="order-input__label"><b>Номер телефона:</b></span><input class="order-input" v-model="userPhone" :disabled="isDisabled" required>
                </div>
                <span><b>Номер заказа: </b>{{orderId.slice(0, 4)}}</span>
        </div>
        <div class="sendOrder-page__order">
            <RouterLink to="/basket" class="sendOrder-page__basket-link">
                <VButtonWhite :title="'отмена'" class="sendOrder-page__deny-button"></VButtonWhite>
            </RouterLink>
            <VButtonRed :title="'оплатить'" class="sendOrder-page__button" :click="'pay'" @pay="openPayModal"></VButtonRed>
        </div>
        <VPayModal
            :isVisible="isModalVisible"
            :title="modalTitle"
            @close="closeModal"
        ></VPayModal>
    </div>
</template>

<script>

// import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import VPizzaBasketCard from '../components/VPizzaBasketCard.vue'
import VHeader from '../components/VHeader.vue';
import VButtonWhite from '../components/VButtonWhite.vue';
import VButtonRed from '../components/VButtonRed.vue';

import axios from 'axios';
import VPayModal from '../components/VPayModal.vue';

export default {
    name: 'SendOrderPage',
    components: {
    // ArrowLeftSVG,
        VPizzaBasketCard,
        VHeader,
        VButtonWhite,
        VButtonRed,
        VPayModal,
    },
    data() {
        return {
            order: [],
            user: [],
            error: null, 
            isModalVisible: false,
            modalTitle: '',
            orderSumm: null,
            isDisabled: false,
            userAddress: null,
            userPhone: null,
            orderId: null,
        };
    },
    methods: {
        async getOrderId() {
            try {
                const response = await axios.get('http://localhost:8001/admin/get_orders_by_status?status=0');
                this.orderId = response.data.data[0].id;
                this.orderSumm = response.data.data[0].summ;
                this.getOrderPizzas(this.orderId);
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; 
                console.error('Ошибка при получении пицц:', error);
            }
        },
        async getOrderPizzas(id) {
            try {
                const response = await axios.get(`http://localhost:8001/admin/get_order_content/${id}`);
                this.order = response.data.data;
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; 
                console.error('Ошибка при получении пицц:', error);
            }
        },
        async getUser() {
            try {
                const response = await axios.get('http://localhost:8001/users/get_user?email=user%40example.com'); // Замените на ваш URL
                this.user = response.data.data;
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        },
        openPayModal() {
            this.modalTitle = 'Заказ оформлен, ожидайте доставку!!!';
            this.isModalVisible = true;
            this.isDisabled = true;
            this.sendOrder();
        },
        closeModal() {
            this.isModalVisible = false;
            this.$router.push('/');
        },
        async sendOrder(){
            console.log(this.user.email,this.userAddress,this.userPhone,);
            try {
                const response = await axios.put(`http://localhost:8001/users/place_order?email=user%40example.com&address=${this.userAddress}&phone=${this.userPhone}`, {
                    email: this.user.email,
                    address: this.userAddress,
                    phone: this.userPhone,
                });
                console.log(response.data);
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        }
    },
    created(){
        this.getOrderId();
        this.getUser()
    }
}
</script>

<style>
.sendOrder-page{
    font-family: Nunito;
    color: #CA151C;
    overflow-x: hidden;
    width: 100%;
    height: 100%;
}
.sendOrder-page__actions{
    display: flex;
    /* justify-content: space-between; */
    justify-content: right;
    margin: 20px 90px;
}
.sendOrder-page__sum{
    font-size: 2rem;
    font-weight: 800;
    display: flex;
    align-items: center;
}
.sendOrder-page__order{
    display: flex;
    justify-content: space-between;
    margin: 50px 90px 30px 90px;
    /* width: 100%; */
}
.sendOrder-page__basket-link, .sendOrder-page__button{
    width: 40%;
}
.sendOrder-page__deny-button{
    width: 100%;
}
.order-input{
    background: none;
    border: solid 3px #BF0200;
    min-height: 30px;
    width: 50%;
    border-radius: 20px;
    font-family: Nunito;
    color: #CA151C;
    font-size: 1.5rem;
    font-weight: 300;
    padding: 3px 20px;
    margin: 10px;
}
.order-input:focus{
    outline: none;
}
.sendOrder__user-info{
    display:flex;
    flex-direction: column;
    margin: 10px 0;
    font-size: 1.7rem;
    justify-content:space-around;
    height: 30%;
    font-weight: 300;
    margin: 40px 90px;
}
.user-info__input{
    display: flex;
    align-items: center;
}
.order-input:disabled{
    outline: none;
    border: none;
}
</style>
