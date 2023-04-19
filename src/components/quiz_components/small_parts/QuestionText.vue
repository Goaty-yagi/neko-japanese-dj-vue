<template>
    <div class="question-wrapper">
        <div class="question-header">
        <i class="q">Q</i>第{{ counter }}問
        </div>
        <div class="question-body">
            <div class="question-label">{{ questionLabel }}</div>
            <div v-if='questionText' class="question-text">{{ questionText }}</div>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        'counter',
        'questionText',
        'questionLabel',
    ],
    data(){
        return {

        }
    },
    mounted() {
       console.log("question-text mounted",this.questionLabel, this.questionText )
    },
    computed:{
        
    },
    methods:{
       
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.question-wrapper {
    width: 95%;
    border: solid rgba(243, 91, 36, 0.808);
    border-radius: 1rem;
    overflow: hidden;
    .question-header {
        background: linear-gradient($base-lite, $base-color);
        color: white;
        padding: 0.5rem;
        font-weight: bold;
        position: relative;
    }
    .question-body {
        background-color: rgb(253, 245, 239);
        padding: 1rem;
        white-space: pre-wrap;
        font-weight: bold;
        .question-label{
            font-size: 1.2rem;
            font-weight: bold;
        }
        .question-text{
            margin-top: 1rem;
        }
    }
    .q {
        position: absolute;
        left: 5%;
        bottom: 2%;
        font-size: 1.5rem;
    }
}

</style>