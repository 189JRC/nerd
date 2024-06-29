<template>
  <div>
    <div id="radio-button-container" class="w-2/5 mx-auto bg-white p-6 rounded-lg shadow-md">

      <div class="flex justify-center">
        <input id="option1" name="options" type="radio" value="article" v-model="desired_action"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option1" class="ml-2 mr-2 block text-gray-700">Article</label>

        <input id="option2" name="options" type="radio" value="youtube_transcript" v-model="desired_action"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option2" class="ml-2 mr-2 block text-gray-700">YouTube Transcript</label>

        <input id="option3" name="options" type="radio" value="twitter" v-model="desired_action"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option3" class="ml-2 mr-2 block text-gray-700">Twitter</label>

        <input id="option3" name="options" type="radio" value="vector_search" v-model="desired_action"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option3" class="ml-2 mr-2 block text-gray-700">Document Vector Search</label>

        <!--NOTE: Consider adding another option to enter raw text-->
      </div>
    </div>

    <div id="search-box-container" class="mb-5">
      <div v-if="desired_action == 'vector_search'"
        class="flex items-center mt-5 p-4 max-w-lg mx-auto dark:bg-white rounded-l shadow-md">
        <input v-model="string_for_vector_comparison" placeholder="Enter search query here"
          class="flex-grow p-3 rounded-l-lg border border-gray-300 focus:outline-none focus:border-blue-500" />
        <button @click="handle_search_request"
          class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
          <!--//@click="investigation.fetch_vector_comparison_data(this.string_for_vector_comparison)"-->
          Find Comparison
        </button>
      </div>

      <div v-else-if="desired_action !== 'vector_search'"
        class="flex items-center mt-5 p-4 w-2/5  mx-auto dark:bg-white rounded-l shadow-md">
        <input v-model="search_target" placeholder="Enter URL or search query here"
          class="flex-grow p-3 rounded-l-lg border border-gray-300 focus:outline-none focus:border-blue-500" />
        <button @click="handle_search_request"
          class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
          Fetch/search
        </button>
        <!--NOTE: Could provide svg images in sequence to guide user through process-->
        <!-- <svg height="100" width="100" >
        <circle cx="50" cy="50" r="20" stroke="black" stroke-width="1" fill="none"/>
      </svg> -->
      </div>
    </div>




    <div class="flex justify-center">
      <button class="bg-blue-300 hover:bg-blue-400 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="investigation.process_text_string_with_nlp_model">Process Text</button>

      <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="highlightText">highlight text</button>

      <button class="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="render_network">build
        network</button>
      <button class="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="unhighlight_text">unhighlight text</button>
    </div>
  </div>
  <br>
  <hr>
  <br>

  <div v-if="desired_action == 'vector_search'" ref="highlighted_text_container" @mouseup="handle_mouse_selection"
    class="relative isolate w-4/5 h-[300px] rounded-xl pl-5 pb-5 pr-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
    <!-- <h1 class="text-dark-grey text-2xl">VECTOR SEARCH</h1>
    <button @click="request_document_records()"
      class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
      get docs
    </button> {{ document_record_metadata }}
    Enter a potential detail to find a match in your document base.... e.g. 'he attended a festival'}-->
    <div ref="chunk_container" v-html="investigation.current_chunk">

    </div>
    <!-- {{  }}
      <li v-for="result in investigation.vector_comparison_metadata.top_most_similar">
        <p><strong>TEXT</strong>{{ result.doc }}</p>
        <p><strong>Similarity score</strong>{{ result.similarity }}</p>
        <p><strong>Sentence match</strong>{{ result.sentence }}</p>
        <p><strong>Document Source:</strong>{{ result.doc_metadata.source }}</p>
      </li> -->

    <!-- <li v-for="(value, key) in investigation.vector_comparison_metadata" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </li> -->
  </div>

  <div v-else ref="highlighted_text_container" @mouseup="handle_mouse_selection"
    class="relative isolate w-4/5 h-[300px] rounded-xl pl-5 pb-5 pr-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
    <br>

    <div ref="chunk_container" v-html="investigation.current_chunk">


    </div>
    <div class="absolute bottom-0 left-0 w-full flex justify-between items-center bg-white p-4">
      <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="see_previous_chunk">
        < </button>{{ chunk_index + 1 }} / {{ this.investigation.text_chunks.length }}

          <!-- <button class="bg-blue-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
            @click="highlightText">view full text</button> -->
          <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
            @click="see_next_chunk">></button>
    </div>

  </div>
  <div v-if="show_popup" :style="popup_style" class="popup">
    <p><strong>{{ popup_text }}</strong><button class="ml-12 p-2 bg-gray-300" @click="closePopup()">X</button></p>
    <hr>
    <br>
    <button v-if="potential_entity" class="bg-green-500" @click="mark_as_significant('entity')">Significant
      entity?</button><br>
    <button v-if="potential_detail" class="bg-green-500" @click="mark_as_significant('detail')">Significant
      Detail?</button><br>
    <button v-if="already_significant" class="bg-orange-500" @click="make_insignificant">Not significant?</button>
  </div>

  <!--DEBUG-->
  <!-- <div class="flex">
    <div class="mt-5 p-4 max-w-md mx-auto dark:bg-gray-200 rounded-l shadow-md">
      <h1 class="text-3xl">DEBUG</h1>
      <h5 class="text-dark-grey text-2xl">All entities</h5>
      <ul>
        <li v-for="entity in investigation.entities" :key="entity.text">
          {{ entity }}
        </li>
      </ul>
    </div>
    <div class="mt-5 p-4 max-w-md mx-auto dark:bg-gray-200 rounded-l shadow-md">
      <h5 class="text-dark-grey text-2xl">Significant Details</h5>
      <ul>
        <li v-for="significant_detail in investigation.significant_details" :key="significant_detail.text">
          {{ significant_detail }}
        </li>
      </ul>
    </div>
    <div class="mt-5 p-4 max-w-md mx-auto dark:bg-gray-200 rounded-l shadow-md">
      <h5 class="text-dark-grey text-2xl">Diagram Entities</h5>

      <ul>
        <li v-for="diagram_entity in diagram_entities" :key="diagram_entity.text">
          {{ diagram_entity }}
        </li>

      </ul>
    </div>
  </div> -->


  <div class="flex">
    <div class="mt-5 p-4 w-[400px] mx-auto dark:bg-gray-200 rounded-xl pl-5 pb-5 pr-5 shadow-md">
      <h5 class="text-dark-grey text-2xl">All entities</h5>
      <div class="col-3">
        <draggable class="list-group" :list="investigation.entities" group="people" itemKey="name">
          <template #item="{ element, index }">
            <div v-if="element.label == 'PERSON'"
              class="list-group-item mb-1 bg-blue-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ index }} {{ element.label }}</div>
            <div v-else
              class="list-group-item mb-1 bg-blue-300 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ index }} {{ element.label }}</div>
          </template>
        </draggable>
        <h5 class="text-dark-grey text-2xl">All details</h5>
        <draggable class="list-group" :list="investigation.significant_details" group="people" itemKey="name">
          <template #item="{ element, index }">
            <div v-if="element.label == 'SIGNIFICANT'"
              class="list-group-item mb-1 bg-blue-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ index }} {{ element.label }}</div>
            <div v-else
              class="list-group-item mb-1 bg-blue-300 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ index }} {{ element.label }}</div>
          </template>
        </draggable>
      </div>
    </div>
    <div id="network" class="w-4/5 h-500 border border-blue-500 rounded mx-auto my-4"
      style="height: 500px; width: 1000px">
    </div>
    <div class="mt-5 p-4 w-[400px] mx-auto dark:bg-gray-200 rounded-xl  pl-5 pb-5 pr-5  shadow-md">
      <h5 class="text-dark-grey text-2xl">Diagram entities</h5>
      <div class="col-3">
        <draggable class="list-group" :list="diagram_entities" group="people" itemKey="name">
          <template #item="{ element, index }">
            <div v-if="element.label == 'PERSON'"
              class="list-group-item mb-1 bg-blue-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ index }} {{ element.label }}</div>
            <div v-else
              class="list-group-item mb-1 bg-blue-300 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ index }} {{ element.label }}</div>
          </template>
        </draggable>
      </div>
    </div>
  </div>
  <br>
  <br>
  <br>
</template>
<script>
import { Network, DataSet } from 'vis-network/standalone/umd/vis-network.min.js';
import { ref, onMounted, nextTick } from 'vue';
import draggable from 'vuedraggable'
//import nestedDraggable from "./infra/nested";

export default {
  name: "two-lists",
  display: "Three Lists",
  order: 1,
  components: {
    draggable,
  },
  name: "nested-draggable",
  props: {
    investigation: {
      type: Object
    },
  },
  data() {
    return {
      document_record_metadata: 0,
      string_for_vector_comparison: null,
      diagram_entities: [
        { name: "test", id: 1 },
      ],
      list2: [
        { name: "Juan", id: 5 },
        { name: "Edgard", id: 6 },
        { name: "Johnson", id: 7 }
      ],
      chunk_index: 0,
      show_popup: false,
      data_entity_selected_for_relevance: "ZZZ",
      // diagram_entities: [{ "label": "GPE", "name": "Tenerife" },
      // { "label": "PERSON", "name": "Jay Slater" },
      // { "label": "DATE", "name": "19-year-old" }],
      search_target: "https://www.telegraph.co.uk/world-news/2024/06/24/jay-slater-missing-update-parents-release-cctv-tenerife/",
      highlighted_text: null,
      selected_text: null,
      youtube_url: null,
      desired_action: "article",
      data_source_option: null,
      already_significant: false,
      potential_entity: false,
      potential_detail: false
    };
  },
  updated() {
    this.add_event_listeners_for_highlighting();
    //console.log(">>>", this.$refs.chunk_container)
  },
  methods: {
    async handle_search_request() {
      console.log("handle_search_request called")
      if (this.desired_action === "vector_search") {
        await this.investigation.fetch_and_process_doc_data(this.search_target = null, this.desired_action, this.string_for_vector_comparison)
        
        this.investigation.text_chunks = this.investigation.vector_comparison_metadata.top_most_similar
        console.log(this.investigation.vector_comparison_metadata.top_most_similar)
        const chunk = [this.investigation.vector_comparison_metadata.top_most_similar[0].similarity, this.investigation.vector_comparison_metadata.top_most_similar[0].doc,
        this.investigation.vector_comparison_metadata.top_most_similar[0].similarity]
        this.investigation.current_chunk = chunk

      } else {
        await this.investigation.fetch_and_process_doc_data(this.search_target, this.desired_action)

      }
    },
    async request_document_records() {
      this.document_record_metadata = await this.investigation.get_document_records()
      console.log(this.document_record_metadata)
    },
    render_network() {
      console.log("build network")
      const nodes = [];
      const edges = [];
      const nodeMap = new Map(); // To track node ids

      // Function to add nodes if they don't exist
      const addNode = (id, label) => {
        if (nodeMap.has(id) == false) {
          nodeMap.set(id, { id: nodeMap.size + 1, label });
          nodes.push({ id: nodeMap.size, label });
        }
      };

      // Process entities to create nodes
      // console.log("raw", this.diagram_entities[0])

      console.log("processed", this.diagram_entities)
      this.diagram_entities.forEach((entity) => {
        console.log(entity, entity.name, entity.label)
        addNode(entity.name, `${entity.label}\n(${entity.name})`);
      });

      // Create edges based on narrative structure
      let lastEntity = null;
      this.diagram_entities.forEach((entity) => {
        if (lastEntity) {
          edges.push({
            from: nodeMap.get(lastEntity.name).id,
            to: nodeMap.get(entity.name).id
          });
        }
        lastEntity = entity;
      });

      const container = document.getElementById('network');
      const data = {
        nodes: nodes,
        edges: edges
      };
      const options = {
        nodes: {
          shape: 'dot',
          size: 10
        },

        physics: {
          stabilization: {
            enabled: true,
            iterations: 200,
            updateInterval: 25
          },
          solver: 'barnesHut',
          barnesHut: {
            gravitationalConstant: -5000,
            centralGravity: 0.1,
            springLength: 95,
            springConstant: 0.01,
            damping: 0.89,
            avoidOverlap: 0.5
          }
        },
        manipulation: {
          enabled: true,
          addNode: function (nodeData, callback) {
            nodeData.label = "New Node";
            callback(nodeData);
          },
          editNode: function (nodeData, callback) {
            //TODO: Make this draggable/ dropable
            nodeData.label = prompt("Enter new label", nodeData.label);
            callback(nodeData);
          },
          addEdge: function (edgeData, callback) {
            if (edgeData.from !== edgeData.to) {
              alert("Cannot connect node to itself.");
              callback(edgeData);
            }
          },
          editEdge:
            function (edgeData, callback) {
              // Prompt the user for a new label for the edge
              const newLabel = prompt("Enter new label for the edge:", edgeData.label || "");

              // If a label is provided, set it on the edgeData
              if (newLabel !== null) {
                edgeData.label = newLabel;
              }

              // Call the callback function with the updated edgeData
              callback(edgeData);
            },
          // {
          //   editWithoutDrag: function (data, callback) {
          //     callback(data);
          //   }
          // },
          deleteNode: function (data, callback) {
            callback(data);
          },
          deleteEdge: function (data, callback) {
            callback(data);
          },
          controlNodeStyle: {
            // Control node style for editing edges
            shape: "dot",
            size: 6,
            color: {
              background: "red",
              border: "black",
            },
            borderWidth: 2,
            borderWidthSelected: 2,
          },
        }
      };
      new Network(container, data, options);
    },
    unhighlight_text() {
      //run through chunk container
      //match any strings with investigation entities
      //extend string to cover <span> and </span>


      //const spans = chunk_div.querySelectorAll('span');
      // console.log(spans)
      // spans.forEach(highlighted_span_element => {
      //   console.log(highlighted_span_element.outerHTML)
      //   chunk_div.innerHTML.replace(highlighted_span_element, console.log(highlighted_span_element.textContent))})
      const spans = this.$refs.chunk_container.querySelectorAll('span');
      console.log(spans, spans.length)

      for (let counter = 0; counter < spans.length; counter++) {
        this.$refs.chunk_container.innerHTML = this.$refs.chunk_container.innerHTML.replace(`<span class="indicator">`, "")
        this.$refs.chunk_container.innerHTML = this.$refs.chunk_container.innerHTML.replace(`</span>`, "")
      }

      for (let counter = 0; counter < spans.length; counter++) {
        this.$refs.chunk_container.innerHTML = this.$refs.chunk_container.innerHTML.replace(`<span class="detail">`, "")
        this.$refs.chunk_container.innerHTML = this.$refs.chunk_container.innerHTML.replace(`</span>`, "")
      }

      this.investigation.current_chunk = this.$refs.chunk_container.innerHTML

      console.log(this.$refs.chunk_container.innerHTML)


    },
    highlightText() {
      console.log("highlightText called")
      //run through removing spans to reset....
      console.log(this.investigation.entities)

      let highlighted = this.investigation.current_chunk;
      this.investigation.entities.forEach(entity => {
        const regex = new RegExp(`\\b${entity.name}\\b`, 'g');
        console.log(entity.name)
        const replacement = `<span class="indicator">${entity.name}</span>`;
        highlighted = highlighted.replace(regex, replacement);
      });

      this.investigation.significant_details.forEach(entity => {
        const regex = new RegExp(`\\b${entity.name}\\b`, 'g');
        console.log(entity.name)
        const replacement = `<span class="detail">${entity.name}</span>`;
        highlighted = highlighted.replace(regex, replacement);
      });

      this.investigation.text_chunks[this.chunk_index] = highlighted
      this.investigation.current_chunk = this.investigation.text_chunks[this.chunk_index]
    },

    add_event_listeners_for_highlighting() {
      const indicators = this.$refs.highlighted_text_container.querySelectorAll('.indicator');
      this.$nextTick(() => { //next tick defers execution
        indicators.forEach(indicator => {
          indicator.removeEventListener('click', this.handle_indicator_click);
          indicator.addEventListener('click', this.handle_indicator_click);
        });
      });
    },
    handle_indicator_click(event) {
      this.popup_text = event.target.textContent;
      this.data_entity_selected_for_relevance = event.target.getAttribute("data-entity")
      this.show_popup = true;
      this.popup_style = {
        position: 'relative',
        top: `${event.clientY - 50}px`,
        left: `${event.clientX - 50}px`
      };
    },
    mark_as_significant(type) {
      // popup text is the highlighted word!¬
      console.log("TYPE+", type)
      let new_significant_object

      if (type == 'entity') {
        console.log(this.popup_text)
        new_significant_object = {
          label: "ENTITY",
          name: `${this.popup_text}`
        }
      } else if (type == 'detail') {
        console.log(this.popup_text)
        new_significant_object = {
          label: "SIGNIFICANT",
          name: `${this.popup_text}`
        }
      }
      // this.diagram_entities.push(new_significant_object) //`{"label":"SIGNIFICANT", "name":"${this.popup_text}"}`)
      if (new_significant_object && type == 'entity') {
        this.investigation.entities.push(new_significant_object) //`{"label":"SIGNIFICANT", "name":"${this.popup_text}"}`)
      } else if (new_significant_object && type == 'detail') {
        this.investigation.significant_details.push(new_significant_object)
      } else {
        console.log("No new entities or significant details created")
      }
      this.highlightText()
      this.closePopup();
    },
    make_insignificant() {
      // TODO: might be less bug prone to resort the ents list with filter method here instead.
      // BIG TODO: Need to gether bunch these terms up and send them to the back end to make search queries out of.
      // console.log(this.diagram_entities)
      this.$refs
      for (let ent_index = 0; ent_index < this.investigation.entities.length; ent_index++) {
        console.log(this.investigation.entities[ent_index])
        if (this.investigation.entities[ent_index].name == this.popup_text) {
          console.log("found")
          this.investigation.entities.splice(ent_index, 1)
        }
      }
      this.unhighlight_text()
      // this.highlightText()
      // console.log(this.popup_text)
      this.closePopup();
    },
    closePopup() {
      this.show_popup = false;
      this.currentSpan = null;
      this.already_significant = false
    },
    handle_mouse_selection(event) {
      console.log("Squeek!")
      console.log(event)
      const selection = document.getSelection();
      const selected_text = selection.toString();
      console.log(selected_text)
      const entities = this.investigation.entities;
      //if selected_text is a 'name' in this.investigation.entities 
      //popup buttons need to reflect this - 'not relevant?'
      //if selected_text is a 'name' in this.investigation.significant_details 
      //popup buttons need to reflect this - 'not relevant?'
      //if selected_text is not present in either it needs:
      //popup buttons: 'significant fact?' 'significant entity?'
      this.already_significant = false
      this.potential_entity = true
      for (const entity_keys in this.investigation.entities) {
        if (this.investigation.entities[entity_keys].name === selected_text) {
          this.already_significant = true
          this.potential_entity = false
        } else {
          this.potential_detail = true
          for (const entity_keys in this.investigation.relevant_details) {
            if (this.investigation.entities[entity_keys].name === selected_text) {
              this.relevant_detail = true
            } else {
              this.potential_detail = false
            }
          }
        }
      }

      if (selected_text.length < 3) {
        return
      } else {
        console.log(selected_text)
        this.show_popup = true
        this.popup_text = selected_text
        this.popup_style = {
          position: 'absolute',
          top: `${event.clientY}px`,
          left: `${event.clientX}px`
        };
      }
    },
    see_next_chunk() {
      if (this.chunk_index < this.investigation.text_chunks.length) {
        this.chunk_index += 1
        this.investigation.current_chunk = this.investigation.text_chunks[this.chunk_index]
      }
    },
    see_previous_chunk() {
      if (this.chunk_index > 0 && this.chunk_index < this.investigation.text_chunks.length + 1) {
        this.chunk_index -= 1
        this.investigation.current_chunk = this.investigation.text_chunks[this.chunk_index]
      }
    }
  }
};
</script>
<style>
.significant {
  background-color: green;
}

.person {
  background-color: pink;
}

.gpe {
  background-color: pink;
}

.date {
  background-color: pink;
}

.loc {
  background-color: pink;
}

.indicator {
  background-color: pink;
}

.detail {
  background-color: yellow;
}

.popup {
  background-color: white;
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
</style>