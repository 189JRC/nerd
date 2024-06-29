
class Investigation {
    constructor(domain_origin) {
        console.log("INV CREATED")
        this.domain_origin = domain_origin
        this.investigation = 'investigation'
        this.text_chunks = []
        this.current_chunk = ""
        this.selected_model = "spacy"
        this.significant_entities = []
        this.entities = []
        this.significant_details = []
        this.vector_comparison_metadata = ["NO DATA"]
        
    }
    async get_document_records() {
      try {
          const response = await fetch('http://localhost:5000/get_document_records', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            },
            // body: JSON.stringify({ text: "text" })
          });
  
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
  
          const document_record_metadata = await response.json();
          return document_record_metadata
          // this.make_significant_entities(data)
  
        } catch (error) {
          console.error('There was a problem with the fetch. Error:', error);
        }
      }
    reset_state() {
        this.highlighted_text = ""
        this.text_chunks = ""
    }
    async fetch_and_process_doc_data(target_url, desired_action, string_to_vectorise=null) {
      // send params for a request, either a url for an article scrape/youtube transcription
      // or a query string to search the existing document base
      // returns text chunks of a doc object or text chunks with metadata for a vector similarity comparison
      console.log("fetch_and_process_doc_data called for", desired_action)  
      this.reset_state()
        if (string_to_vectorise == null) {
          var body = JSON.stringify({ url: target_url, desired_action: desired_action })
        } else if (string_to_vectorise != null) {
          var body = JSON.stringify({ url: null, desired_action: desired_action, string_for_vector_comparison: string_to_vectorise})
        }
        try {
            
            const response = await fetch(`${this.domain_origin}/fetch_and_process_doc_data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
               
                body: body
                
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            // set conditional on desired_action not stringtovectorise
            if (string_to_vectorise == null) {
            const data = await response.json();
            
            // article text is now a list of
            this.text_chunks = data.text_chunks;
            this.current_chunk = this.text_chunks[0]
            console.log("!!!", data.text_chunks, data.named_entities)
            } else if (string_to_vectorise != null) {
              const data = await response.json();
              console.log("!!!", data)
              // const vector_comparison_metadata = await response.json();
              // this.vector_comparison_metadata = vector_comparison_metadata;
              // console.log(typeof(this.vector_comparison_metadata))
              // console.log(this.vector_comparison_metadata.top_most_similar)
            }

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
    // async fetch_vector_comparison_data(string_for_vector_comparison) {
    //   console.log("CALLED fetch_vector_comparison_data")
    //     try {
    //       const response = await fetch('http://localhost:5000/vector_similarity', {
    //         method: 'POST',
    //         headers: {
    //           'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ string_for_vector_comparison: string_for_vector_comparison, params: "none yet" })
    //       });
  
    //       if (!response.ok) {
    //         throw new Error('Network response was not ok ' + response.statusText);
    //       }
  
    //       const vector_comparison_metadata = await response.json();
    //       this.vector_comparison_metadata = vector_comparison_metadata;
    //       // this.make_significant_entities(data)
  
    //     } catch (error) {
    //       console.error('There was a problem with the fetch. Error:', error);
    //     }

    // }
    async process_text_string_with_nlp_model() {
        console.log("CALLED process_text_string_with_nlp_model")
        try {
          const response = await fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: this.current_chunk, model: this.selected_model })
          });
  
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
  
          const data = await response.json();
          this.entities = data;
          // this.make_significant_entities(data)
  
        } catch (error) {
          console.error('There was a problem with the fetch. Error:', error);
        }
      }
    reset_state() {
        this.highlighted_text = ""
        this.text_chunks = ""
    }
    // make_significant_entities(entity_objects) {
    //     entity_objects.forEach((entity) => {
    //       this.significant_entities.push(entity);
    //     });
    //   }
}

export default Investigation