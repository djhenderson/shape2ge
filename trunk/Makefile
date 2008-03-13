all: ./standalone/shape2ge-frontend.py ./standalone/shape2ge-engine.py

./standalone/shape2ge-frontend.py: ./src/xmlwriter.py ./src/styles.py ./src/frontend.py
	echo "#!/usr/bin/python" > ./standalone/shape2ge-frontend.py
	cat ./src/xmlwriter.py ./src/styles.py ./src/frontend.py | grep -v "AUTO_REMOVED" >> ./standalone/shape2ge-frontend.py
	chmod +x ./standalone/shape2ge-frontend.py

./standalone/shape2ge-engine.py: ./src/xmlwriter.py ./src/styles.py ./src/vec.py ./src/shapeobjects.py ./src/engine.py
	echo "#!/usr/bin/python" > ./standalone/shape2ge-engine.py
	cat ./src/xmlwriter.py ./src/styles.py ./src/vec.py ./src/shapeobjects.py ./src/engine.py | grep -v "AUTO_REMOVED" >> ./standalone/shape2ge-engine.py
	chmod +x ./standalone/shape2ge-engine.py

clean:
	rm ./standalone/shape2ge-engine.py
	rm ./standalone/shape2ge-frontend.py
