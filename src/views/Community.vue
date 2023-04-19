<template>
  <!-- this scroll fixed should be change -->
  <div
    class="community-wrapper scroll_area"
  >
    <div class="main-wrapper">
      <div
        class="community-container"
        v-if="handleQuestions && !$store.state.isLoading"
      >
        <div class="header-flex">
          <h1 class="title-white">質問板</h1>
          <div v-if="emailVerified" class='user-font-container'>
            <i
            @click="goAccount()"
            class="fas fa-user user-font"
            >
            </i>
            <i v-if="notificationAPI" class="fas fa-exclamation"></i>
          </div>
        </div>
        <form class="search-wrapper" @submit.prevent="splitSearch()">
          <i @click="splitSearch" class="fas fa-search"
            ><input class="search" v-model="search" type="text"
          /></i>
        </form>

        <div class="question-box" v-if="showQuestionStatus.search == false">
          <p class="word">わからない事があったら質問してみよう。</p>
          <button
            class="btn-base-white-db-sq"
            @click="handleShowCreateQuestion"
          >
            質問する
          </button>
        </div>

        <div class="select-wrapper" v-if="showQuestionStatus.search == false">
          <button
            @click="questionHandler('recent')"
            :class="{
              'btn-tr-white-base-cir': showQuestionStatus.recent == false,
              'btn-tr-black-baselite-cir': showQuestionStatus.recent,
            }"
          >
            最近の投稿
          </button>
          <button
            @click="questionHandler('reccomend')"
            :class="{
              'btn-tr-white-base-cir': showQuestionStatus.reccomend == false,
              'btn-tr-black-baselite-cir': showQuestionStatus.reccomend,
            }"
          >
            おすすめの<wbr />投稿
          </button>
        </div>
        <div class="question-wrapper">
          <CreateQuestion
            v-if="showCreateQuestion"
            :parentTagDict="parentTagDict"
            @getDetail="getDetail"
            @handleShowConfirm="handleShowConfirm"
            @handleShowCreateQuestion="handleShowCreateQuestion"
          />
          <transition name="notice">
            <NotVerified
              v-if="showEmailVerified"
              @handleShowEmailVerified="handleShowEmailVerified"
            />
          </transition>
          <transition name="notice">
            <NotLogin
              v-if="showNotLogin"
              @handleShowNotLogin="handleShowNotLogin"
            />
          </transition>

          <!-- here is for searched questions -->
          <div v-if="showQuestionStatus.search">
            <div class="search-title">{{ String(wordList) }}の検索結果</div>
            <div v-if='questions.results.length' class="sort-burger">
              <div class="sort">
                 <p v-if="!currentSort" class='defa-text'>関連度順</p>
                <FormSelect
                :choicesArray='sortList'
                :clickTypeConfig='clickTypeConfig'
                :bulletObj='bulletObj'
                optionAlign="center-on-left"
                ref='select'
              />
              </div>
            </div>
            <div class="no-found" v-if="questions.results == false">
              <p class="no-found-word">お探しの質問は見つかりませんでした。</p>
              <div class="route">
                <div @click="goHome()">
                  <i class="fas fa-home"></i>
                  <p>ホームへ戻る</p>
                </div>
                <div @click="handleShowQuestionStatusSearch()">
                  <i class="far fa-comments"></i>
                  <p>質問板へ戻る</p>
                </div>
              </div>
            </div>
            <AbstractQuestionList  v-if="!spinner" :questions="questions" ref="child" />
            <div v-if="spinner" class="is-loading-bar has-text-centered middle-loading" v-bind:class="{'is-loading': spinner }">
                <div class="lds-dual-ring"></div>
            </div>
          </div>
          <!-- here for general questions -->
          <AbstractQuestionList
            v-if="showQuestionStatus.search == false"
            :questions="handleQuestions"
            ref="child"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NotVerified from "@/components/login/NotVerified.vue";
import NotLogin from "@/components/login/NotLogin.vue";
import { router } from "../main.js";
import CreateQuestion from "@/components/board/CreateQuestion.vue";
import Search from "@/components/board/Search.vue";
import AbstractQuestionList from "@/components/board/AbstractQuestionList.vue";
import FormSelect from "@/components/parts/FormSelect.vue";
export default {
  components: {
    CreateQuestion,
    Search,
    NotVerified,
    NotLogin,
    AbstractQuestionList,
    FormSelect
  },
  data() {
    return {
      questions: "",
      temporaryQuestion: "",
      search: "",
      wordList: [],
      parentTagDict: {},
      showCreateQuestion: false,
      showEmailVerified: false,
      showNotLogin: false,
      showConfirm: false,
      userTagList: [],
      searchedQuestion: "",
      onAnswerOrReply: false,
      spinner:false,
      currentSort:'',
      sortList:['新しい順','古い順','解決済み','回答受付中','閲覧数','ハートの数','回答数'],
      clickTypeConfig:{
        showArrow: true,
        arrowPlace:'right',
        function: this.getSelectedItem
       },
      bulletObj:{
        type: "same",
        bullet: "・",
      },
      showQuestionStatus: {
        recent: true,
        reccomend: false,
        search: false,
      },
      styles: {
        position: "",
        top: "",
      },
    };
  },
  created() {
    console.log("CREATED");
    this.$store.dispatch("getNotificationApi");
  },
  async beforeMount() {
    await this.getQuestion();
  },
  mounted() {
    this.scrollTop();
    this.handleOnAnswerOrReply();
    this.$store.dispatch("getRelatedQuestion");
    this.showEmailVerified = false;
    // this.$store.commit("showModalFalse");
    // this.$store.commit("fixedScrollFalse");
  },
  beforeUnmount() {
    // this.$store.commit("showModalFalse");
    // this.$store.commit("fixedScrollFalse");
  },
  computed: {
    user() {
      return this.$store.state.signup.user;
    },
    notification() {
      return;
    },
    reccomendedQuestion() {
      return this.$store.getters.gettersReccomendedQuestion;
    },
    emailVerified() {
      return this.$store.getters.getEmailVerified;
    },
    fixedScroll() {
      return this.$store.getters.fixedScroll;
    },
    notificationAPI() {
      return this.$store.getters.notificationApi;
    },
    handleQuestions() {
      if (this.showQuestionStatus.recent) {
        this.questions = this.temporaryQuestion;
        return this.questions;
      } else if (this.showQuestionStatus.reccomend) {
        this.questions = this.reccomendedQuestion;
        return this.questions;
      } else if (this.showQuestionStatus.search) {
        this.questions = this.searchedQuestion;
        return this.questions;
      }
    },
  },
  methods: {
    async getQuestion() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/board/question/list")
        .then((response) => {
          this.temporaryQuestion = response.data;
        })
        .catch((e) => {
          let logger = {
            message: "in Community/getQuestio. couldn't get Question",
            path: window.location.pathname,
            actualErrorName: e.name,
            actualErrorMessage: e.message,
          };
          this.$store.commit("setLogger", logger);
          this.$store.commit("setIsLoading", false);
          router.push({ name: "ConnectionError" });
        });
      this.$store.commit("setIsLoading", false);
      this.getParentTag();
    },
    async getParentTag() {
      await axios
        .get("/api/board/parent-tag")
        .then((response) => {
          let parentTags = response.data;
          this.getParentTagDict(parentTags);
        })
        .catch((e) => {
          let logger = {
            message: "in Community/getParentTag. couldn't get ParentTag",
            path: window.location.pathname,
            actualErrorName: e.name,
            actualErrorMessage: e.message,
          };
          this.$store.commit("setLogger", logger);
          this.$store.commit("setIsLoading", false);
          router.push({ name: "ConnectionError" });
        });
    },
    handleOnAnswerOrReply() {
      if (
        this.$store.getters.handleOnAnswer ||
        this.$store.getters.handleOnReply
      ) {
        this.onAnswerOrReply = true;
      }
    },
    async getSearchQuestion() {
      console.log("GSEARCH", this.wordList);
      await axios
        .get(`/api/board/question/search/?keyword=${this.wordList}&sort=${this.currentSort}`)
        .then((response) => {
          this.searchedQuestion = response.data;
          this.questionHandler("search");
        })
        .catch((e) => {
          console.log("ER", e);
          let logger = {
            message:
              "in Community/getSearchQuestion. couldn't get SearchQuestion",
            path: window.location.pathname,
            actualErrorName: e.name,
            actualErrorMessage: e.message,
          };
          this.$store.commit("setLogger", logger);
          this.$store.commit("setIsLoading", false);
          router.push({ name: "ConnectionError" });
        });
    },
    async splitSearch() {
      if (this.search) {
        this.currentSort = ''
        this.wordList = [];
        let letterList = [];
        this.search = this.search.trim();
        this.search = this.search.split("");
        for (let i of this.search) {
          if ((i === " " && letterList[0]) || (i === "　" && letterList[0])) {
            this.wordList.push(letterList.join(""));
            letterList = [];
          } else if (i === " " || i === "　") {
          } else {
            letterList.push(i);
          }
        }
        this.wordList.push(letterList.join(""));
        letterList = [];
        this.search = "";
        this.$store.commit("setIsLoading", true);
        await this.getSearchQuestion();
        this.$store.commit("setIsLoading", false);
      }
    },
    getParentTagDict(parentTags) {
      for (let i of parentTags) {
        this.parentTagDict[i.parent_tag] = i.center_tag;
      }
    },
    handleShowCreateQuestion() {
      if (this.emailVerified && this.user) {
        this.showCreateQuestion = !this.showCreateQuestion;
      } else if (!this.emailVerified && this.user) {
        this.handleShowEmailVerified();
      } else {
        this.handleShowNotLogin();
      }
    },
    handleShowEmailVerified() {
      this.showEmailVerified = !this.showEmailVerified;
    },
    handleShowNotLogin() {
      this.showNotLogin = !this.showNotLogin;
    },
    handleShowConfirm() {
      this.showConfirm = !this.showConfirm;
    },
    getDetail(slug) {
      router.push(`/board-detail/${slug}`);
    },
    questionHandler(key) {
      // recieve "recent" or "reccomend" to change status
      if (key != "search") {
        this.$refs.child.bottomScrollActionHandlerTrue();
      }
      for (let i of Object.keys(this.showQuestionStatus)) {
        if (i == key) {
          this.showQuestionStatus[i] = true;
        } else {
          this.showQuestionStatus[i] = false;
        }
      }
    },
    handleShowQuestionStatusSearch() {
      this.showQuestionStatus.search = false;
      this.showQuestionStatus.recent = true;
    },
    async getSelectedItem() {
      // sortList:['新しい順','古い順','解決済み','回答受付中','閲覧数','ハートの数','回答数'],
      switch(this.$refs.select.chosenItem){
        case '新しい順':
          this.currentSort = 'new'
          break
        case '古い順':
          this.currentSort = 'old'
          break
        case '解決済み':
          this.currentSort = 'solved'
          break
        case '回答受付中':
          this.currentSort = 'unsolved'
          break
        case '閲覧数':
          this.currentSort = 'viewed'
          break
        case 'ハートの数':
          this.currentSort = 'liked'
          break
        case '回答数':
          this.currentSort = 'answered'
          break
      }
      // const sortWordList = ['solved', 'unsolved', 'liked', 'answered', 'viewed', 'new', 'old' ]
      console.log(this.currentSort)
      this.spinner = true
      await this.getSearchQuestion()
      this.spinner = false
    },
    goHome() {
      router.push("/");
      this.$store.commit("reset");
    },
    goAccount() {
      router.push("/board/account");
    },
    scrollTop() {
      window.scrollTo({
        top: 0,
      });
    },
  },
};
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
.scroll {
  position: fixed;
}
.community-wrapper {
  display: flex;
  flex-direction: column;
  height: auto;
  min-height: 80vh;
  width: 100vw;
  align-items: center;
  .main-wrapper {
    .community-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      .header-flex {
        display: flex;
        justify-content: center;
        position: relative;
        width: 100%;
        .user-font-container{
          position: absolute;
          width: 90%;
          .user-font {
            position: absolute;
            right: 0;
            margin-right: 1rem;
            margin-top: 1rem;
            font-size: 2rem;
            color: $dark-blue;
            transition: 0.5s;
          }
          .user-font:hover {
            color: gray;
          }
          .fa-exclamation {
            position: absolute;
            width: 1rem;
            height: 1rem;
            right: 0;
            margin-right: 0.6rem;
            margin-top: 0.5rem;
            font-size: 0.5rem;
            border: 0.1rem solid red;
            border-radius: 50vh;
            // padding: 0.3rem;
            padding-top: 0.1rem;
            padding-bottom: 0.1rem;
            padding-left: 0.3rem;
            padding-right: 0.3rem;
            color: red;
            background: $back-white;
          }
        }
      }
      .search-wrapper {
        border: solid $base-color;
        border-radius: 50vh;
        width: 70%;
        height: 2.5rem;
        background: $back-white;
        display: flex;
        align-items: center;
        .fa-search {
          width: 100%;
          margin-left: 1rem;
          padding-right: 1rem;
          transition: 0.5s;
          color: rgb(165, 165, 165);
          .search {
            border: none;
            padding-left: 0.5rem;
            background: $back-white;
            width: 90%;
          }
        }
        .fa-search:focus-within {
          color: rgb(80, 80, 80);
        }
      }
      .question-box {
        border: solid $base-color;
        border-radius: 0.5rem;
        width: 95%;
        height: 10rem;
        background: rgb(252, 252, 252);
        margin: 1rem;
        .word {
          margin: 1rem;
          font-size: 1.5rem;
        }
        .btn-base-white-db-sq {
          padding-top: 0.5rem;
          padding-bottom: 0.5rem;
          padding-left: 1rem;
          padding-right: 1rem;
          font-size: 1rem;
          font-weight: bold;
        }
      }
      .select-wrapper {
        .btn-tr-black-baselite-cir {
          padding-top: 0.5rem;
          padding-bottom: 0.5rem;
          font-size: 0.8rem;
          margin-right: 0.1rem;
        }
        .btn-tr-white-base-cir {
          padding-top: 0.5rem;
          padding-bottom: 0.5rem;
          font-size: 0.8rem;
          margin-left: 0.1rem;
        }
      }
      .question-wrapper {
        margin: 1rem;
        width: 95%;
        .search-title {
          // margin-top: 2rem;
          margin-bottom: 1rem;
          border-bottom: 0.2rem solid $dark-blue;
          display: inline-block;
          color: white;
          font-size: 1.5rem;
        }
        .sort-burger {
          width: 100%;
          display: flex;
          margin-right: 1rem;
          margin-bottom: 1rem;
          justify-content: flex-end;
          .sort:hover {
            background: #656565;
          }
          .sort {
            position: relative;
            width: 150px;
            height: 30px;
            border: solid gray;
            padding: 0.6rem;
            border-radius: 5px;
            font-size: 0.8rem;
            color: #e9e9e9;
            background: #3c3c3c;
            transition: .3s;
            .defa-text {
              position: absolute;
              font-weight: bold;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
            }
          }
        }
        .no-found {
          .no-found-word {
            margin-top: 0.5rem;
            color: whitesmoke;
            margin-bottom: 1rem;
          }
          .route {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            color: gray;
            div {
              margin: 1rem;
              color: whitesmoke;
            }
            div:hover {
              color: rgb(191, 191, 191);
              transition: 0.3s;
            }
          }
        }
      }
    }
  }
}
.is-loading-bar {
  margin-top: 2rem;
}
</style>