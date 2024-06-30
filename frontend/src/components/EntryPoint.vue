<template>
  <div class="flex justify-center items-center">
    <div class="w-4/5">


      <!-- Top Header -->
      <div class="mt-5 p-6 dark:bg-gray-600 rounded-xl shadow-md flex items-center space-x-4">
        <h1 class="text-white text-4xl">N.E.R.D (Named Entity Recognition Diagramiser)</h1>
      </div>

      <br>

      <!-- Main Content -->
      <div class="flex">
        <!-- Left side: Header (Already centered) -->
        <div class="flex w-full flex-col">
          <!-- Radio Buttons -->

          <div id="radio-button-container" class="w-full bg-white p-6 rounded-lg shadow-md mt-4">
            <div class="flex justify-center">
              <input id="option1" name="options" type="radio" value="article" v-model="desired_action"
                class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
              <label for="option1" class="ml-2 mr-2 block text-gray-700">Article Scrape</label>

              <input id="option2" name="options" type="radio" value="youtube_transcript" v-model="desired_action"
                class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
              <label for="option2" class="ml-2 mr-2 block text-gray-700">YouTube Transcript</label>

              <!-- <input id="option3" name="options" type="radio" value="twitter" v-model="desired_action"
              class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
            <label for="option3" class="ml-2 mr-2 block text-gray-700">Twitter</label> -->

              <input id="option4" name="options" type="radio" value="vector_search" v-model="desired_action"
                class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
              <label for="option4" class="ml-2 mr-2 block text-gray-700">Document Vector Search</label>
            </div>
          </div>


          <!-- Search Box -->
          <div id="search-box-container" class="mb-5">
            <div v-if="desired_action == 'vector_search'"
              class="flex items-center mt-5 p-4 w-4/5 mx-auto dark:bg-white rounded-l shadow-md">
              <input v-model="string_for_vector_comparison" placeholder="Enter search query here"
                class="flex-grow p-3 rounded-l-lg border border-gray-300 focus:outline-none focus:border-blue-500" />
              <button @click="fetch_and_process_doc_data"
                class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
                Find Comparison
              </button>
            </div>

            <div v-else-if="desired_action !== 'vector_search'"
              class="flex items-center mt-5 p-4 w-4/5 mx-auto dark:bg-white rounded-l shadow-md">
              <input v-model="search_target" placeholder="Enter URL or search query here"
                class="flex-grow p-3 rounded-l-lg border border-gray-300 focus:outline-none focus:border-blue-500" />
              <button @click="fetch_and_process_doc_data"
                class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
                Fetch and Process
              </button>
              <select id="options" @click="get_document_records" name="options"
                class="ml-2 px-4 py-3 h-[48px] bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
                <option value="">Document Records</option>
                <option v-for="record in investigation.document_records" value="option1">{{ record.substring(0, 30) }}
                </option>
              </select>
            </div>

          </div>

          <!-- Action Buttons -->
          <div class="flex justify-center">




            <button class="bg-blue-200 hover:bg-blue-300 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
              @click="investigation.process_text_string_with_nlp_model">View Document Record</button>

            <button class="bg-blue-300 hover:bg-blue-400 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
              @click="investigation.process_text_string_with_nlp_model">Process Text</button>

            <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
              @click="highlightText">Highlight Text</button>

            <button class="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
              @click="build_network">Build Network</button>

            <button class="bg-blue-800 hover:bg-blue-900 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
              @click="unhighlight_text">Unhighlight Text</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <br>
  <hr>
  <br>

  <div v-if="desired_action == 'vector_search'" ref="highlighted_text_container" @mouseup="handle_mouse_selection"
    class="relative isolate w-4/5 h-[325px] rounded-xl pl-5 pb-5 pr-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
    <!-- <h1 class="text-dark-grey text-2xl">VECTOR SEARCH</h1>
    <button @click="request_document_records()"
      class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
      get docs
    </button> {{ document_record_metadata }}
    Enter a potential detail to find a match in your document base.... e.g. 'he attended a festival'}-->

    <div ref="chunk_container" v-html="investigation.current_chunk"></div>
    <!-- <div v-if="search_complete">
      <p><strong>TEXT</strong>{{ investigation.current_chunk.doc }}</p>
      <p><strong>TITLE:</strong>{{ investigation.current_chunk.doc_metadata }}</p>
        <p><strong>SENTENCE:</strong>{{ investigation.current_chunk.sentence }}</p>
          <p><strong>SIMILARITY:</strong>{{ investigation.current_chunk.similarity }}</p>
        </div> -->

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

  <div v-else ref="highlighted_text_container" @mouseup="handle_mouse_selection"
    class="relative isolate w-4/5 h-[325px] rounded-xl pl-5 pb-5 pr-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
    <br>
    <div
      class="relative isolate w-4/5 h-[65px] rounded-xl pl-5 pb-7 pt-2 pr-5 mb-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
      <strong>Text Summary:</strong> {{ investigation.text_summary }}
    </div>
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
  <br>

  <div class="flex relative isolate w-4/5 rounded-xl pl-5 pb-5 pr-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
    <div class="mt-5 p-4 w-1/5 mx-auto dark:bg-gray-200 rounded-xl pl-5 pb-5 pr-5 shadow-md">
      <h5 class="text-dark-grey text-2xl">All entities</h5>
      {{ investigation.entities }}
      <div class="col-3">
        <draggable class="list-group" :list="investigation.entities" group="people" itemKey="name">
          <template #item="{ element, index }">
            
            <div v-if="element.label == 'PERSON'"
              class="flex list-group-item mb-1 bg-blue-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }}  {{ element.label }}</div>
            <div v-else
              class="list-group-item mb-1 bg-blue-300 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }}  {{ element.label }}</div>
          </template>
        </draggable>
        <h5 class="text-dark-grey text-2xl">All details</h5>
        {{ investigation.significant_details }}
        <draggable class="list-group" :list="investigation.significant_details" group="people" itemKey="name">
          <template #item="{ element, index }">
            <div v-if="element.label == 'SIGNIFICANT'"
              class="list-group-item mb-1 bg-blue-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ element.label }}</div>
            <div v-else
              class="list-group-item mb-1 bg-blue-300 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ element.label }}</div>
          </template>
        </draggable>

      </div>
    </div>
    <div id="network" class="w-4/5 h-500 border mt-10 border-blue-500 rounded mx-auto my-4"
      style="height: 500px; width: 1000px">
    </div>

    <div class="mt-5 p-4 w-1/5  mx-auto dark:bg-gray-200 rounded-xl  pl-5 pb-5 pr-5  shadow-md">
      <h5 class="text-dark-grey text-2xl">Diagram entities</h5>
      {{ diagram_entities }}
      <div class="col-3">



        <draggable class="list-group" :list="diagram_entities" group="people" itemKey="name">
          <template #item="{ element, index }">
           
            <div v-if="element.label == 'PERSON' || element.label == 'IDENTIFIED PERSON'"
              class="list-group-item mb-1 bg-blue-500 text-black px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
              {{ element.name }} {{ element.label }}
              <div>Locations:</div>


              <div class="dark:bg-gray-200 rounded-xl ">
                {{ element.name }}

                <draggable @change="update_network_data(element.name, 'location', $event)"
                  v-if="element.label == 'PERSON' || element.label == 'IDENTIFIED PERSON'" class="list-group" :list="element.relevant_details.locations"
                  group="people" itemKey="name">
                  <template #item="{ element, index }">
                    <div 
                      class="mt-2 bg-blue-300 text-black px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
                      {{ element.name }} </div>

                  </template>
                </draggable>


                <br>
                <br>
              </div>
              <div>Relevant details:</div>


              <div class="dark:bg-gray-200 rounded-xl ">
                {{ element.name }}

                <draggable @change="update_network_data(element.name, 'relevant_details', $event)"
                  v-if="element.label == 'PERSON' || element.label == 'IDENTIFIED PERSON'" class="list-group" :list="element.relevant_details.details"
                  group="people" itemKey="name">
                  <template #item="{ element, index }">
                    <div
                      class="mt-2 bg-blue-300 text-black px-4 py-2 rounded-md shadow-md hover:bg-blue-700 cursor-pointer">
                      {{ element.name }} </div>

                  </template>
                </draggable>


                <br>
                <br>
              </div>
            </div>
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
      search_complete: false,
      show: "NONE",
      temp_relevant_details_drag: [
        {
          name: "placeholder"
        },
        {
          name: "placeholder2"
        }
      ],
      temp_locations_drag: [],
      document_record_metadata: 0,
      string_for_vector_comparison: null,
      diagram_entities: [
        {
          name: "Drag entities here",
        },
      ],
      chunk_index: 0,
      show_popup: false,
      data_entity_selected_for_relevance: "ZZZ",
      // diagram_entities: [{ "label": "GPE", "name": "Tenerife" },
      // { "label": "PERSON", "name": "Jay Slater" },
      // { "label": "DATE", "name": "19-year-old" }],
      search_target: null,
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
  watch: {
    test_drag: {
      handler(newVal) {
        // Update the relevant details in diagram_entities based on changes in test_drag
        //this.updateDiagramEntities();
      },
      deep: true,
    },
  },
  updated() {
    this.add_event_listeners_for_highlighting();
    //console.log(">>>", this.$refs.chunk_container)
  },
  methods: {
    update_network_data(name, entry_point, event) {

      const parent = this.diagram_entities.find(entity => entity.name === name);

      // if (parent) {
      //   const dragged_entity_object = event.added ? event.added.element : 0;
      //   if (entry_point == 'location') {

      //   parent.relevant_details.locations.push(dragged_entity_object)
      //   } else if (entry_point == 'relevant_details') {

      //     parent.relevant_details.details.push(dragged_entity_object)
      //   }
      // }
    },
    // log(event) {
    //   console.log(event.target)

    // },
    add(e) {
      console.log("add", e.target)
    },
    async fetch_and_process_doc_data() {
      console.log("fetch_and_process_doc_data called in component")
      if (this.desired_action === "vector_search") {
        await this.investigation.fetch_and_process_doc_data(this.search_target = null, this.desired_action, this.string_for_vector_comparison)

        //this is a bit hacky...
        //alternative would be to process template in back end which doesn't seem right
        //the issue is the html formatting with highlight/unhighlight
        this.format_vector_search_responses_for_display()
        //this.investigation.text_chunks = this.investigation.vector_comparison_data.top_most_similar
        // console.log(this.investigation.vector_comparison_metadata.top_most_similar)
        const chunk = [this.investigation.vector_comparison_data.top_most_similar[0]]
        // const this.investigation.vector_comparison_metadata.top_most_similar[0].similarity]

        // this.investigation.current_chunk = chunk
        // this.investigation.text_chunks = this.investigation.vector_comparison_data.top_most_similar
        // console.log(chunk)
        this.search_complete = true

      } else {
        await this.investigation.fetch_and_process_doc_data(this.search_target, this.desired_action)

      }
    },
    format_vector_search_responses_for_display() {
      this.investigation.text_chunks = []
      for (let index = 0; index < 10; index++) {
        //each chunk is a js object with .text .similarity .title .sentence
        //need to make it into html
        //const chunk = this.investigation.vector_comparison_data.top_most_similar[index]
        console.log(this.investigation.vector_comparison_data.top_most_similar[index].similarity)



        var chunk_html =
          `<p><strong>Similarity Score: </strong>${this.investigation.vector_comparison_data.top_most_similar[index].similarity}</p>
        <p><strong>Document Origin: </strong>${this.investigation.vector_comparison_data.top_most_similar[index].doc_metadata}</p>
        <p><strong>String match: </strong>${this.investigation.vector_comparison_data.top_most_similar[index].sentence}</p>
        <p><strong>Text: </strong>${this.investigation.vector_comparison_data.top_most_similar[index].doc.substring(0, 1000)}</p>`


        this.investigation.text_chunks.push(
          chunk_html

        )
        console.log("added new chunk for", index)
        if (index == 0) {
          this.investigation.current_chunk = chunk_html
        }
      }
    },
    async get_document_records() {
      this.document_record_metadata = await this.investigation.get_document_records()
      console.log(this.document_record_metadata)
    },
    build_network() {
      // TODO: This needs to be a child component!
      console.log("build network")
      const nodes = []
      const edges = []
      //map is like a js object, but maintains the order of its entries
      //it also has methods such as .has which is handy
      const node_map = new Map()

      //function to add nodes if they don't exist
      const add_node = (id, label, title) => {
        if (node_map.has(id) == false) {
          node_map.set(id, { id: node_map.size + 1, label, title });
          nodes.push({ id: node_map.size, label, title });
        }
      };

      const central_node = this.diagram_entities[0]


      this.diagram_entities.forEach((diagram_entity) => {

        let title = ''
        // if the entity has been given relevant details for location or details
        // map the value to a variable, then apply it to the title 
        // (title is the hover tooltip)
        // else add the node but dont give it a title
        if (diagram_entity.relevant_details) {
          const locations = diagram_entity.relevant_details.locations.map(location => location.name).join(', ');
          const details = diagram_entity.relevant_details.details.map(detail => detail.name).join(', ');
          title = `Locations: ${locations}\nDetails: ${details}`
          add_node(diagram_entity.name, `${diagram_entity.name}\n${diagram_entity.label}`, title)
        } else {
          add_node(diagram_entity.name, `${diagram_entity.name}\n${diagram_entity.label}`)
        }

        if (central_node && diagram_entity.name !== central_node.name) {
          edges.push({
            from: node_map.get(central_node.name).id,
            to: node_map.get(diagram_entity.name).id
          });
        }
      });


      //grab the network diagram element and apply options.
      const container = document.getElementById('network');
      const data = {
        nodes: nodes,
        edges: edges
      };
      const options = {
        nodes: {
          shape: 'dot',
          size: 10,
          font: {
            multi: 'html',
            size: 12
          }
        },

        interaction: {
          tooltipDelay: 200,
          hover: true
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
          // these functions allow for gui features built into vis js
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
              //allow labelling a link/edge
              const new_label = prompt("Enter new label for the edge:", edgeData.label || "");
              if (new_label !== null) {
                edgeData.label = new_label;
              }
              callback(edgeData);
            },
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
          label: "PERSON",
          name: `${this.popup_text}`,
          relevant_details: {locations: [], details: []}
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
      console.log("called next chunk")
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

::ng-deep div.vis-tooltip {
  position: absolute;
  visibility: hidden;
  padding: 5px;
  white-space: nowrap;
  color: #000000;
  background-color: #f5f4ed;

  -moz-border-radius: 3px;
  -webkit-border-radius: 3px;
  border-radius: 3px;
  border: 1px solid #808074;

  box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
  pointer-events: none;

  z-index: 5;
}
</style>