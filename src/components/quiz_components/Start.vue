<template>
    <div class="start-wrapper">
        <div class="main-wrapper">
            <div class="quiz-title-container">
                <div v-if="forQuizPageInfo.all==false" class="not-all">
                    <div class="start-grade">
                        <GradeIcon 
                        :grade='forQuizPageInfo.grade'/>
                        <p>{{ forQuizPageInfo.grade }}</p>
                    </div>
                    <p class="field-and-option">{{ forQuizPageInfo.field }}</p>
                    <p class="field-and-option"> {{forQuizPageInfo.option}}問題</p>
                </div>
                <div v-if="forQuizPageInfo.all" class="dojo">{{ forQuizPageInfo.grade }}道場</div>
                <p class="start-length">全{{ showQuestionLength }}問</p>
            </div>
            <div class="button-container">
                <div @click="closeStart()" class="btn-base-white-db-sq">
                    START
                </div>
            </div>
            <div class="start-notification-container">
                <div class="start-notification"
                v-for="(des,index) in forQuizPageInfo.description"
                v-bind:key="index"
                >
                    {{ des }}
                </div>
            </div>
        </div>
      
    </div>
</template>

<script>
import GradeIcon from "@/components/quiz_components/small_parts/GradeIcon.vue";
export default {
    components: {
        GradeIcon
    },
    props:[
        'questionLength',
        'forQuizPageInfo',
        'quizType',
        'testOrInit'
    ],

    data(){
        return{
        }
    },
    beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    mounted(){
        console.log("MO", this.forQuizPageInfo)
        this.scrollTop()
    },
    computed:{
        showQuestionLength() {
            if(this.testOrInit) {
                return '???'
            } else {
                return this.questionLength
            }
        }
    },
    methods:{
        goQuiz(){
            this.$emit('goQuiz')
        },
        closeStart(){
            this.$emit('closeStart')
        },
        scrollTop(){
            window.scrollTo({
            top: 0,
            });
        },
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.start-wrapper{
    .main-wrapper{
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
        .quiz-title-container{
            width: 80%;
            border: solid $base-color;
            border-radius: 0.5rem;
            background: $back-white;
            margin-top: 3rem;
            overflow: hidden;
            .not-all{
                width: 100%;
                .start-grade{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 60px;
                    font-size: 1.5rem;
                    font-weight: bold;
                    background: $background-bottom-right;
                    border-bottom: solid $base-color;
                    color: white; 
                    .start-icon {
                        margin-right: 0.5rem;
                        margin-bottom: 0.1rem;
                    }
                }
                .field-and-option{
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                    font-weight: bold;
                }
            }
            .start-length{
                border: solid $middle-blue;
                border-radius: 10px;
                padding-right: 0.9rem;
                padding-left: 0.9rem;
                margin-bottom: 1rem;
                display: inline-block;
                font-size: 1.5rem;
                font-weight: bold;
                background: #d53c4f;
                color: whitesmoke;
            }
        }
        .dojo{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60px;
            font-size: 1.5rem;
            font-weight: bold;
            background: $background-bottom-right;
            border-bottom: solid $base-color;
            color: white; 
        }
        .button-container{
            margin-top: 2rem;
            margin-bottom: 2rem;
            .btn-base-white-db-sq{
                padding-top: 0.3rem;
                padding-bottom: 0.3rem;
                padding-right: 0.8rem;
                padding-left: 0.8rem;
                font-size: 1.5rem;
                font-weight: bold;
            }
        }
        .start-notification{
            text-align: left;
            width: 100%;
            color: white;
            margin-top: 2rem;
            white-space: pre-wrap;
        }
    }
}
.start-notification-container {
    display: flex;
    align-items: center;
    flex-direction: column;
}
@media (max-width: 480px) {
  .start-notification{
        max-width: 80%;
        }
}
</style>