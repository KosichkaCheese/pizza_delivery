<template>
    <div class="basket-page">
        <VHeader :title="'корзина'" :toLink="'/'"></VHeader>
        <template>
            <!-- <div class="pizza-container" > -->
                <VPizzaBasketCard
                    v-for="(position, index) in order" 
                    :key="index" 
                    :name="position.pizza_name" 
                    :cost="position.pizza_cost"
                    :amount="position.count"
                ></VPizzaBasketCard>
            <!-- </div> -->
      </template>
        
        <div class="basket-page__actions">
            <!-- <VButtonWhite :title="'очистить корзину'"></VButtonWhite> -->
            <span class="basket-page__sum">итого: {{ orderSumm}} руб.</span>
        </div>
        <div class="basket-page__order">
            <RouterLink to="/send_order" class="basket-page__order-link">
                <VButtonRed :title="'оформить заказ'" class="basket-page__order-button"></VButtonRed>
            </RouterLink>
        </div>
    </div>
</template>

<script>

// import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import VPizzaBasketCard from '../components/VPizzaBasketCard.vue'
import VHeader from '../components/VHeader.vue';
// import VButtonWhite from '../components/VButtonWhite.vue';
import VButtonRed from '../components/VButtonRed.vue';

import axios from 'axios';

export default {
    name: 'BasketPage',
    components: {
    // ArrowLeftSVG,
        VPizzaBasketCard,
        VHeader,
        // VButtonWhite,
        VButtonRed,
    },
    data() {
        return {
            order: [],
            error: null, // Переменная для хранения ошибок
            isModalVisible: false,
            modalTitle: '',
            modalMessage: '',
            orderSumm: null,
            // orderId: null,
        };
    },
    methods: {
        async getOrderId() {
            try {
                const response = await axios.get('http://localhost:8001/admin/get_orders_by_status?status=0');
                const orderId = response.data.data[0].id;
                this.orderSumm = response.data.data[0].summ;
                this.getOrderPizzas(orderId);
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; 
                console.error('Ошибка при получении пицц:', error);
            }
        },
        async getOrderPizzas(id) {
            try {
                const response = await axios.get(`http://localhost:8001/admin/get_order_content/${id}`);
                this.order = response.data.data;
                // console.log(this.order);
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; 
                console.error('Ошибка при получении пицц:', error);
            }
        },
        // openModal(name, description, id) {
        //     this.modalTitle = name
        //     this.modalMessage = description;
        //     this.pizzaId = id;
        //     this.isModalVisible = true;

        //     // console.log(333);
        // },
        // closeModal() {
        //     this.isModalVisible = false;
        // }
    },
    created(){
        this.getOrderId();
    }
}
</script>

<style>
.basket-page{
    font-family: Nunito;
    color: #CA151C;
    overflow-x: hidden;
    width: 100%;
    height: 100%;
}
.basket-page__actions{
    display: flex;
    /* justify-content: space-between; */
    justify-content: right;
    margin: 20px 90px;
}
.basket-page__sum{
    font-size: 1.8rem;
    font-weight: 800;
    display: flex;
    align-items: center;
}
.basket-page__order{
    display: flex;
    justify-content: center;
    margin-bottom: 50px;
    width: 100%;
}
.basket-page__order-link{
    width: 40%;
}
.basket-page__order-button{
    width: 100%;
}
</style>
