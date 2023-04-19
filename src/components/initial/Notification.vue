<template>
    <div class='notification-wrapper l-wrapper'>
        <div class='notice-wrapper'>
            <img class='image' src="@/assets/logo.png">
            <p class='text2'>登録すると…</p>
            <div class='block'>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="far fa-lightbulb" id='in-font'></i>
                        <div class='text'>
                            <p>色んなクイズができる</p>
                        </div>
                    </i>       
                </div>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="fas fa-crown" id='in-font'></i>
                        <div class='text'>
                            <p>自分のレベルを管理できる</p>
                        </div>
                    </i>       
                </div>
            </div>
            <div class='block'>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="fas fa-award" id='in-font'></i>
                        <div class='text'>
                            <p>毎日、実力を確認できる</p>
                        </div>
                    </i>       
                </div>
                <div class='font-inline'>
                    <i id='font' class="fas fa-cog">
                        <div class='circle'/>  
                        <i class="fas fa-robot" id='in-font'></i>
                        <div class='text'>
                            <p>コミュニティに参加できる</p>
                        </div>
                    </i>       
                </div>
            </div>
            <div class='buttons'>
                <router-link @click='closeConf' to='/' class='btn-litegray-black-gray-sq' >登録しない</router-link>
                <router-link  to='/signup' class='btn-litegray-black-gray-sq' >登録する</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            top:0
        }
    },
    mounted() {
        this.top = window.scrollY
        document.body.style.top = `-${window.scrollY}px`;
        document.body.style.position = 'fixed'
    },
    beforeUnmount() {
        document.body.style.position = ''
        window.scrollTo(0, this.top)
    },
    methods:{
        closeConf(){
            this.$emit('close')
            this.$store.commit('reset')
        },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";


.notification-wrapper{
    display: flex;
    align-items: center;
    justify-content: center;
    }
    .notice-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        display:inline-block;
        max-width: 450px;
    }
    .image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .text-container{
        display: flex;
        justify-content: center;
        .text1{
            font-size:1.2rem;
            font-weight: bold;
            color: red;
            margin-bottom: 0.5rem;
            border: solid red;
            width: 80%;
        }
    }
    .text2{
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.7rem;
    }
    .block{
        display:flex;
        justify-content: center;
        align-items: center;
        margin-top:-3%;
    }
    .font-inline{
        flex-basis:auto;
            }.font-inner{
                color:initial;
                position:absolute;
                font-size:1rem;
                color:$back-white;
            }
    #in-font{
        font-size:initial;
        color:initial;
        font-size:2.5rem;
        color:$back-white;
        position:absolute;
        top: 25%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .text{
        color:initial;
        position:absolute;
        top:55%;
        padding-left:20%;
        padding-right:20%;
        font-size:1rem;
        font-weight: bold;
        text-align: center;
    }
    #font{
        position:relative;
        font-size:10rem;
        color: $base-color;
        top:auto;
        bottom:auto;

    }.circle{
        position:absolute;
        border:solid $base-color;
        border-radius: 50%;
        background:$base-color;
        margin:auto;
        height: 5rem;
        width: 5rem;
        margin: 0 auto;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .buttons{
        display:flex;
        justify-content: center;
        align-items: center;
        margin:1%;
        margin-bottom:1rem;
        .btn-litegray-black-gray-sq{
            // font-size: 1.5rem;
            margin-left: 0.5rem;
            margin-right: 0.5rem;
        }
    }
    #register-button{
        width: auto;
        font-size:5vw;
        padding:1.5%;
        
    }
</style>