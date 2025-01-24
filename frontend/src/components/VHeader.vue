<template>
    <div class="page__header">
        <RouterLink :to="toLink" class="back_button">
            <ArrowLeftSVG :height="50" :width="50"></ArrowLeftSVG>
        </RouterLink>
        <div class="page__title">
            <span>{{ title }}</span>
        </div>
    </div>
</template>

<script>
import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';

export default {
    name: 'VHeader',
    components: {
        ArrowLeftSVG,
    },
    props:{
        title: String,
        toLink: String,
    }
}

</script>
<style scoped>
.page__header{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-left: 20px;
}
.page__title{
    display: flex;
    align-items: center;
    background-color: #FFE9C1;
    border: 4px solid #CA151C;
    border-radius: 50px;
    width: auto;
    height: auto;
    color: #CA151C;
    margin: 20px;
    font-family: Nunito;
    font-size: 2.7rem;
    font-weight: 800;
    padding: 0 20px;
}
</style>
