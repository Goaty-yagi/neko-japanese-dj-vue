<template>
    <div class='thumbnail-wrapper' :class="{'l-wrapper':selectedFile}">
        <form @submit.prevent='userUpdate'>
            <input id="fileUpload" type="file" accept="image/x-png ,image/jpeg" @change='getImage' hidden enctype="multipart/form-data">
            <div class="cropper-outer-wrapper" v-if="selectedFile">
                <div class='cropperinner-wrapper'>
                    <img ref='image' :src="selectedFile" style="width: 300px; height: 300px;">
                </div>
                <div class="thumbnail-button-container">
                    <button class='btn-tr-white-base-sq thumbnail-cancel-button' @click='chancel'>cancel</button>
                    <button class='btn-base-white-db-sq thumbnail-save-button'>save</button>
                </div>
            </div>
        </form>
        <div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Cropper from 'cropperjs';
export default {
    
    props:[
        "getUser",
        "minContainerWidth",
        "minContainerHeight",
        "imageType",
        "ratio"
    ],
    data(){
        return{
            file:'',
            image:'',
            selectedFile:null,
            compoHandle: false,
            cropper:{},
            destination:{},
            inputFile:'',
            blob:'',
            cropperBorder:'',
            type:'',
            format:'',
            errorMessage:'components/account/Thumbnail',
        }
    },
    mounted(){
        console.log("MOUNGRED", this.user)
        this.top = window.scrollY
        document.body.style.top = `-${window.scrollY}px`;
        document.body.style.position = 'fixed'
        this.autoClick()
    },
    beforeUnmount() {
        console.log("BUM")
        document.body.style.position = ''
        window.scrollTo(0, this.top)
    },
    computed:{
        user(){
            return this.$store.state.signup.user
        },
        width(){
            if(this.minContainerWidth == 800){
                return 800
            }else{
                return 400
            }
        },
        height(){
            if(this.minContainerHeight == 800){
                return 800
            }else{
                return 400
            }
        },
        defaultRatio() {
            if(this.ratio) {
                return this.ratio
            } else {
                return 1
            }
        }
    },
    methods:{
        async getImage(event){
            this.selectedFile = URL.createObjectURL(event.target.files[0])
            this.image = event.target.files[0]
            this.type = this.image.type
            this.format = this.type.split('/')[1]
            await console.log(this.selectedFile)
            this.imageCropper(this.imageType)
        },
        async imageCropper(type){
            this.cropper = new Cropper(this.$refs.image, {
            zoomable: true,
            scalable: false,
            zoomOnTouch: true,
            aspectRatio: this.defaultRatio,
            dragMode: 'move',
            minContainerHeight:this.height,
            minContainerWidth:this.width,
            crop(event) {
                    console.log(event.detail.x);
                    console.log(event.detail.y);
                    console.log(event.detail.width);
                    console.log(event.detail.height);
                    console.log(event.detail.rotate);
                    console.log(event.detail.scaleX);
                    console.log(event.detail.scaleY);
                    if(type == 'thumbnail'){
                        const cropperBorder = document.getElementsByClassName("cropper-view-box","cropper-face")
                        cropperBorder[0].style.borderRadius = '50vh'
                    }
                },
            })
        },
        chancel(){
            this.selectedFile=null
            this.showThumbnailFalse()
        },
        autoClick(){
            document.getElementById("fileUpload").click()
            this.inputFile = document.getElementById("fileUpload");
            document.body.onfocus = this.getEvent
        },
        getEvent(){
            setTimeout(() => {
                if (this.inputFile.value.length) {
                
                } else {
                this.showThumbnailFalse()
                }
                document.body.onfocus = null;
            }, 500);
        },
        openFileOnClick(){
            console.log("openFILECLICK")
            document.getElementById("fileUpload").value = "";
            document.getElementById("fileUpload").files.length = 0;            
            document.getElementById("fileUpload").click();
            if(document.getElementById("fileUpload").files.length >= 1){
                //Do something 
            }
            else{
                this.showThumbnailFalse()
                //Cancel button has been called.
            }
        },
        // getCroppedURL(){
        //     console.log('croppedURL')
        //     document.getElementById('crop-btn').addEventListener('click', function () {
        //     resultImgUrl = this.cropper.getCroppedCanvas().toDataURL();
        //     var result = document.getElementById('result-img');
        //     result.src = resultImgUrl;
        //      });
        // },
        async userUpdate(){
            console.log('clicked')
            if(this.imageType == 'thumbnail') {
                try{
                    const canvas = this.cropper.getCroppedCanvas({
                    width: 500,
                    height: 500,
                    minCropBoxHeight: 300,
                    minCropBoxWidth: 300,
                    maxWidth: 4096,
                    maxHeight: 4096,
                    // fillColor: '#fff',
                    imageSmoothingEnabled: false,
                    imageSmoothingQuality: 'high',
                    });
                await canvas.toBlob(async (blob) => {
                    console.log("toblob",this.image, blob)
                    // debugger
                    const formData = new FormData();
                    formData.append('thumbnail',blob, this.image + '.' + this.format),
                    console.log('getthumb',formData.get('thumbnail'),this.image,blob),
                    axios
                    .patch(`/api/user-patch/${this.getUser.UID}`,
                        formData)
                }, this.type)
                    canvas.toBlob(async (blob) => {
                        const url = URL.createObjectURL(blob)
                        this.user.thumbnail = url
                        this.$emit('imageCreatedHandler')
                        this.showThumbnailFalse()
                    },this.type)
                } catch(e){    
                    console.log("ERROR", e)
                    let logger = {
                        message: this.errorMessage + " userUpdate",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    this.$store.commit('setIsLoading', false)
                    router.push({ name: 'ConnectionError' })
                    this.showThumbnailFalse()
                }
                // this.$router.go({path: this.$router.currentRoute.path, force: true})
            } else {
                console.log('else')
                try{
                    const canvas = this.cropper.getCroppedCanvas({
                    width: 1000,
                    height: 1000,
                    minCropBoxHeight: 300,
                    minCropBoxWidth: 300,
                    maxWidth: 4096,
                    maxHeight: 4096,
                    // fillColor: '#fff',
                    imageSmoothingEnabled: false,
                    imageSmoothingQuality: 'high',
                    });
                canvas.toBlob(async (blob) => {
                    this.setImageBlob(blob)
                    },this.type)
                }
                catch(e){
                    this.showThumbnailFalse()
                    console.log('fale',e)
                }
            }
        },
        setImageBlob(blob){
            this.blob = blob
            let url = URL.createObjectURL(blob)
            this.$emit('setImageBlob',blob, url)
            this.showThumbnailFalse()
        },
        showThumbnailFalse(){
            this.$emit('showThumbnailFalse')
        },
        reload(){
            // this.$store.commit('setIsLoading', false)
            location.reload()
        }
    }
}
</script>

<style  lang="scss">
// not scoped for cropper
@import "style/_variables.scss";

.thumbnail-wrapper{
    position: absolute;
    width: 100%;
    height: 100%;
    /* background: ; */
    overflow:scroll;  
}
.cropper-view-box,
    .cropper-face {
      cursor: grab;
      outline: initial;
    }
    .cropper-face:active {
      cursor: grabbing;
    }
.thumbnail-button-container{
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    .thumbnail-save-button{
        display: flex;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 0.5rem;
        min-width: 5rem;
        min-height: 2rem;
        font-weight: bold;
    }
    .thumbnail-cancel-button{
        display: flex;
        justify-content: center;
        font-size: 1.2rem;
        margin-left: 0.5rem;
        min-width: 5rem;
        min-height: 2rem;
        font-weight: bold;
    }
}
</style>