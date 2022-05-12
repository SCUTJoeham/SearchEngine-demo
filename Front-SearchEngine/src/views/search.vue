<template>
    <el-container>
        <el-header style="padding: 0">
            <el-row>
                <el-col :md="8">
                </el-col>
                <el-col :md="16" style="margin-top: 0.2%">
                    <el-autocomplete
                            v-model="key_word"
                            placeholder="please input search content"
                            :fetch-suggestions="querySearch"
                            @select="handleSelect"
                            :trigger-on-focus="false">
                        <el-button id="search_btn" slot="append" @click="search_btn">Search</el-button>
                        <template slot-scope="{ item }">
                            <div class="title">{{ item.tags }}</div>
                        </template>
                    </el-autocomplete>
                </el-col>
            </el-row>
        </el-header>
        <el-main style="padding: 0">
            <el-row>
                <el-col :md="24">
                    <el-tabs v-model="search_title" @tab-click="handleClick">
                        <el-tab-pane label="          Search Results          " name="one">
                            <el-row>
                                <el-col :md="16" :offset="1">
                                    <div class="news-content"
                                         style="margin-top: 3%"
                                         v-for="text in search_result" :key="text.id">
                                        <div class="news_title" style="margin-top: 1%">
                                            <a :href="text.url" v-html="text.title" target="_blank"/>
                                        </div>
                                        <div class="text-item limit-line" v-html="text.content"/>
                                    </div>
                                </el-col>
                            </el-row>
                        </el-tab-pane>
                    </el-tabs>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script>
    export default {
        name: "Search",
        data() {
            return {
                key_word: '',
                search_title: 'one',
                search_result: [

                ]
            }
        },
        methods: {
            handleClick(tag, event) {
                console.log(tag, event)
            },
            querySearch(queryString, cb) {
                this.axios.get("http://localhost:8888/news/suggest?prefix=" + queryString)
                    .then(resp => {
                        // 调用 callback 返回建议列表的数据
                        cb(resp.data);
                    })
            },
            search_btn(){
                this.axios.get("http://localhost:8000/search/?query=" + this.key_word)
                    .then(resp => {
                      console.log(resp.data.search_result)
                        this.search_result = resp.data.search_result
                    })
            },
            handleSelect(item){
                this.key_word = item.tags
                console.log(item.tags)
            }
        },
        mounted() {
            this.key_word = this.$route.params.key_word
            this.axios.get("http://localhost:8000/search?query=" + this.key_word)
                .then(resp => {
                    this.search_result = resp.data.search_result
                    this.key_word = resp.data.query
                })
        }
    }
</script>

<style scoped>
    /* 搜索按钮 */
    #search_btn {
        background: #409EFF;
        color: whitesmoke;
        border-bottom-left-radius: 0;
        border-top-left-radius: 0;
        height: 40px;
    }

    #search_btn:hover {
        background: #4060ff;
    }

    /* 右边连接 */
    .header-right {
        margin-top: 4%;
        margin-left: 5%;
    }

    /* 新闻内容 */
    .limit-line {
        overflow:hidden;
        text-overflow:ellipsis;
        display:-webkit-box;
        -webkit-box-orient:vertical;
        -webkit-line-clamp:5;
    }
    .text-item {
        margin-top: 1.5%;
    }
</style>