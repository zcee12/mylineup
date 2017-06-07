.PHONY: clean run test

clean:
	rm -rf runtime/

runtime:
	mkdir -p runtime/pending/
	mkdir -p runtime/processed/

run-api-server: runtime
	cd api_server && make run

run-aggregator-service: runtime
	cd aggregator_service && make run

sanity-check:
	curl -H "Content-Type: application/json" \
		-X POST -d '{"event_id":"27082564-glastonbury-festival-2017","artists":["Radiohead", "Muse"]}' \
		http://localhost:5000/api/v1/lineup/recommend
