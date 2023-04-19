<template>
     <AbstractCreateAndConfirm :obj="objForModal" />
</template>

<script>
import axios from 'axios'
import AbstractCreateAndConfirm from "@/components/board/AbstractCreateAndConfirm.vue";
export default {
    components: {
        AbstractCreateAndConfirm,
    },
    data(){
        return{
            errorMessage: 'components/board/Reply',
            objForModal: {
                mainTitle: "コメント",
                title:'',
                text: this.reply,
                userMainText: "返信文",
                placeholder: "返信",
                buttonText: "コメントする",
                cancelFunc: this.cancelFunc,
                buttonFunc: this.addAnswer,
            },
        }
    },
    props:[
        'answerId',
        'reply',
        'handleNotifications'
    ],
    mounted(){
    },
    beforeUnmount(){        
    },
    computed: {
        detailQuestion() {
            return this.$store.getters.getDetailQuestion
        },
    },
    methods:{
        async replyPost(description){
            await axios({
                method: 'post',
                url: '/api/board/reply/create/',
                data: {
                    description: description,
                    user: this.$store.state.signup.user.UID,
                    answer: this.answerId
                }
            })
            .then(async (res) => {
                console.log('then', res.data)
                await this.setReply(res.data)
            })
            .catch((e) => {
                this.$store.commit('setApiError')
            })
        },
        async setReply(reply) {
            const obj = {
                reply:reply,
                answerId: this.answerId
            }
            this.$store.commit("setReplayToAnswer", obj);
        },
        async addAnswer(description){
            this.$store.commit('setIsLoading', true)
            window.scrollTo(0,0)
            await this.replyPost(description)
            this.$store.dispatch("handleNotifications", 'reply')
            this.$emit('getDetail')
            this.$store.commit('setIsLoading', false)
            this.cancelFunc()
        },
        cancelFunc() {
            console.log("CHANCEL")
            this.$emit('handleShowReplyPage')
        }
    }
}
</script>

<style scoped lang='scss'>

</style>