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
                :id="pizza.id"
                @openModal="openModal(pizza.name, pizza.description, pizza.id)"
            ></VPizzaCard>
        </div>
      </template>
    </div>
    <VPizzaInfoModal
      :isVisible="isModalVisible"
      :message="modalMessage"
      :id="pizzaId"
      :title="modalTitle"
      @close="closeModal"
      @openAddModal="openAddModal"
    />
    <VAddModal
        :isVisible="isAddModalVisible"
        :title="addModalTitle"
        @close="closeAddModal"
    ></VAddModal>
  </div>
</template>

<script>

import LogoSVG from '@/img/logoSVG.vue';
import BasketSVG from '@/img/basketSVG.vue';
import LkSVG from '@/img/lkSVG.vue';
import TitleIconSVG from '@/img/titleIconSVG.vue';
import VPizzaCard from '../components/VPizzaCard.vue';
import VPizzaInfoModal from '../components/VPizzaInfoModal.vue';
import VAddModal from '../components/VAddModal.vue';
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
    VAddModal,
  },
  data() {
        return {
            pizzas: [], 
            error: null, 
            isModalVisible: false,
            modalTitle: '',
            modalMessage: '',
            isAddModalVisible: false,
            addModalTitle: '',
            pizzaId: null,
        };
    },
    methods: {
        async getPizzas() {
            try {
                const response = await axios.get('http://localhost:8001/admin/get_pizza_list');
                this.pizzas = response.data.data; 
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message;
                console.error('Ошибка при получении пицц:', error);
            }
        },
        openModal(name, description, id) {
            this.modalTitle = name
            this.modalMessage = description;
            this.pizzaId = id;
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },
        
        openAddModal() {
            console.log(22);
            this.addModalTitle = 'Товар добавлен в корзину!';
            this.isAddModalVisible = true;
        },
        closeAddModal() {
            this.isAddModalVisible = false;
        },

    },
    created(){
        this.getPizzas();
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
  margin-bottom: 5px;
}
.page__menu-content-pizzas{
  margin: 0px 50px;
}
.pizza-container {
  display: flex;
  justify-content: space-between;
  margin: 0 60px;
  flex-wrap: wrap;
} 

</style>
