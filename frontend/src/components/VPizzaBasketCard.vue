<template>
    <div class="pizza-basket-card">
        <div class="pizza-basket-card__pic">
            <img src="../img/pizza.png" class="pizza_pic"/>
        </div>
        <div class="pizza-basket-card__content">
            <div class="pizza-basket-card__content_up">
                <span class="card-title">{{ name }}</span>
                <span class="card-price">{{ cost }} руб.</span>
            </div>
            <div class="pizza-basket-card__content_down">
                <div class="pizza-basket-card__content_down-amount">
                    <div class="amount-button">
                        <ArrowLeftSVG :width="30" :height="30"></ArrowLeftSVG>
                    </div>
                    <span class="basket-card__amount">{{ amount }} шт.</span>
                    <div class="amount-button">
                        <ArrowRightSVG :width="30" :height="30"></ArrowRightSVG>
                    </div>
                </div>
                <TrashSVG></TrashSVG>
            </div>
        </div>
    </div>
</template>

<script>
import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import ArrowRightSVG from '@/img/arrowRightSVG.vue';
import TrashSVG from '@/img/trashSVG.vue';

export default {
    name: 'VPizzaBasketCard',
    components: {
        ArrowLeftSVG,
        ArrowRightSVG,
        TrashSVG,
    },
    props: {
        name: String,
        cost: Number,
        amount: Number
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.pizza-basket-card{
    display: flex;
    align-items: center;
    background-color: #FFEFD2;
    border: 3px solid #BF0200;
    border-radius: 30px;
    padding: 20px;
    font-family: Nunito;
    color: #CA151C;
    margin: 10px 90px;
}
.pizza-basket-card__pic{
    justify-self: left;
}
.pizza_pic{
    height: 145px;
    width: 145px;
}
.pizza-basket-card__content{
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 20vh;
    justify-content: space-between;
    margin-left: 20px;
}
.pizza-basket-card__content_up{
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.pizza-basket-card__content_down{
    display: flex;
    justify-content: space-between;
    min-height: 40px;
}
.basket-card__amount{
    margin: 0 7px;
    font-size: 1.5rem;
    font-weight: 300;
}
.pizza-basket-card__content_down-amount, .amount-button{
    display: flex;
    align-items: center;
}
.card-title{
    font-size: 2.2rem;
}
.card-price{
    font-size: 1.7rem;
    font-weight: 500;
}
</style>
