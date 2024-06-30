
class Investigation {
    constructor(domain_origin) {
        this.domain_origin = domain_origin
        this.investigation = 'investigation'
        this.text_chunks = []
        this.current_chunk = ""
        //this.significant_entities = []
        this.entities = []
        this.significant_details = []
        this.vector_comparison_data = []  
        this.text_summary = "" 
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
          this.document_records = document_record_metadata
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
              this.entities = data.named_entities
              console.log(data.text_summary)
              this.text_summary = data.text_summary

              for (let index=0; index<this.entities.length; index++) {
                if (this.entities[index].label === "PERSON") {
                  this.entities[index].relevant_details = {}
                  this.entities[index].relevant_details.locations = []
                  this.entities[index].relevant_details.details = []
                }
              }
            
            } else if (string_to_vectorise != null) {
              const data = await response.json()
              this.reset_state()
              console.log("!!!", data)
              console.log(data)
              // data is object
              // best_doc_metadata = origin
              // best_doc_text = full text
              // highest_similarity
              // most_similar_span
              this.vector_comparison_data = data
       
              //console.log(this.vector_comparison_metadata.top_most_similar)
            }

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
    reset_state() {
        this.highlighted_text = ""
        this.text_chunks = ""
    }
}

export default Investigation