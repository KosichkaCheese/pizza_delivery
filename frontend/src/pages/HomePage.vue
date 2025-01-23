<template>
  <div id="home_page">
    <div class="page__header">
      <RouterLink to="/LK" class="lk_button">
        <LkSVG></LkSVG>
      </RouterLink>
      <LogoSVG></LogoSVG>
      <RouterLink to="/basket" class="basket_button">
        <BasketSVG></BasketSVG>
      </RouterLink>
    </div>
    <div class="page__menu-title">
      <span>наше меню</span>
    </div>
    <div class="page__menu-content">
      <TitleIconSVG></TitleIconSVG>
      <span class="mini-title">супер популярное!</span>
    </div>
    <div class="page__menu-content-pizzas">
      <template>
        <div class="pizza-container" >
            <VPizzaCard 
                class="pizza-card" 
                v-for="(pizza, index) in pizzas" 
                :key="index" 
                :name="pizza.name" 
                :price="pizza.cost"
                @openModal="openModal(pizza.description, pizza.id)"
            ></VPizzaCard>
        </div>
      </template>
    </div>
    <VPizzaInfoModal
      :isVisible="isModalVisible"
      :message="modalMessage"
      :id="pizzaId"
      @close="closeModal"
    />
  </div>
</template>

<script>

import LogoSVG from '@/img/logoSVG.vue';
import BasketSVG from '@/img/basketSVG.vue';
import LkSVG from '@/img/lkSVG.vue';
import TitleIconSVG from '@/img/titleIconSVG.vue';
import VPizzaCard from '../components/VPizzaCard.vue';
import VPizzaInfoModal from '../components/VPizzaInfoModal.vue';
import axios from 'axios';

export default {
  name: 'HomePage',
  components: {
    LogoSVG,
    BasketSVG,
    LkSVG,
    TitleIconSVG,
    VPizzaCard,
    VPizzaInfoModal,
  },
  data() {
        return {
            pizzas: [], // Массив для хранения пицц
            error: null, // Переменная для хранения ошибок
            isModalVisible: false,
            modalTitle: '',
            modalMessage: '',
            pizzaId: null,
        };
    },
    methods: {
        async test_request() {
            try {
                const response = await axios.get('http://localhost:8001/admin/get_pizza_list'); // Замените на ваш URL
                this.pizzas = response.data.data; // Сохраняем данные в состоянии компонента
                // console.log(this.pizzas);
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        },
        openModal(description, id) {
            this.modalMessage = description;
            this.pizzaId = id;
            this.isModalVisible = true;

            // console.log(333);
        },
        closeModal() {
            this.isModalVisible = false;
        }
    },
    created(){
        this.test_request();
    }
}
</script>

<style>
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  src: url(../assets/Nunito-Black.ttf) format('truetype');
}
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 500;
  src: url(../assets/Nunito-Bold.ttf) format('truetype');
}
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 300;
  src: url(../assets/Nunito-SemiBold.ttf) format('truetype');
}
body {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  /* text-align: center; */
  background-color: #FFF9ED;
}
#home_page{
  width: 100%;
  height: 100%;
  
}
.page__header{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.basket_button,.lk_button{
  background-color: #FFE9C1;
  border: 4px solid #CA151C;
  border-radius: 50px;
  width:65px;
  height: 65px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 50px;
  /* justify-self: flex-end; */
}
.page__menu-title{
  background-color: #FFE9C1;
  border: 4px solid #CA151C;
  border-radius: 50px;
  width: 95%;
  height: auto;
  color: #CA151C;
  margin: 30px 50px;
  text-align: center;
  font-family: Nunito;
  font-size: 2.7rem;
  font-weight: 800;
  justify-self: center;
}
.page__menu-content{
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-family: Nunito;
  font-size: 2.2rem;
  color: #CA151C;
  margin-left: 130px;
}
.mini-title{
  margin-left: 20px;
  margin-bottom: 20px;
}
.page__menu-content-pizzas{
  display: flex;
  justify-content: space-evenly;
  margin: 0px 50px;
}
.pizza-container {
  display: flex;
  /* display: flex; */
  justify-content: space-between;
  margin: 0 50px;
  flex-wrap: wrap;
}

</style>
