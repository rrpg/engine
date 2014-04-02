#
# Targets:
#  - clean	Delete .pyc files
#  - locale-template            Generate .pot file for current project domain
#  - locale-update              Update .po files of from current .pot for all available local domains
#  - locale-deploy              Generate all .mo files
#  - locale-deploy-fuzzy        Generate all .mo files with fuzzy
#  - locale-clean               Remove all .mo and .po files

PYTHON = python

PROJECT_NAME = "rRpg Engine"
PROJECT_LOCALE_DOMAIN = "message"

# Path
ROOT = .
PROJECT_LOCALE_PATH = $(ROOT)/locales

# Files Finder
FIND_LOCALE_SRC = find $(PROJECT_LOCALE_PATH) -type f -iname '*.po' -not -name ".*"
FIND_LOCALE_FILES = find $(PROJECT_LOCALE_PATH) -type f -iname '*.po' -o -iname '*.mo' -not -name ".*"
FIND_PYTHON_LOCALE_FILES = find $(ROOT) -type f -iname '*.py'

# Locales
LOCALE_GETTEXT_DIR 	= LC_MESSAGES
LOCALE_DOMAINS 		= $(PROJECT_LOCALE_DOMAIN)# time validate

all: locale-deploy
	git submodule init
	git submodule update

# Clean the working directory
clean:
	find . -name "*.pyc" -delete
	find . -name __pycache__ -delete

#
# Locale
#

# Generate .pot file for current project domain
locale-template:
	@echo "----------------"
	@echo "Build GetText POT files for $(PROJECT_NAME):"
	@echo "" > $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$(PROJECT_LOCALE_DOMAIN).pot
	@$(FIND_PYTHON_LOCALE_FILES) | xgettext --from-code=UTF-8 -L PYTHON -j -F -o $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$(PROJECT_LOCALE_DOMAIN).pot -f -
	@msguniq $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$(PROJECT_LOCALE_DOMAIN).pot -o $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$(PROJECT_LOCALE_DOMAIN).pot
	@echo "Building $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$(PROJECT_LOCALE_DOMAIN).pot"
	@echo "done"

# Update .po files of from current .pot for all available local domains
locale-update:
	@echo "----------------"
	@echo "Update GetText PO files from POT files:"
	@for o in $(LOCALE_DOMAINS); do \
		for i in `find $(PROJECT_LOCALE_PATH) -maxdepth 1 -mindepth 1 -type d -not -name "dist" -not -name ".*"`; do \
			if [ -e "$$i/$(LOCALE_GETTEXT_DIR)/$$o.po" ] ; then \
				echo "Updating $$i/$(LOCALE_GETTEXT_DIR)/$$o.po"; \
				msgmerge -N --previous $$i/$(LOCALE_GETTEXT_DIR)/$$o.po $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$$o.pot -o $$i/$(LOCALE_GETTEXT_DIR)/$$o.po; \
			else mkdir $$i/$(LOCALE_GETTEXT_DIR)/ -p; \
				msginit -l `echo "$(ROOT)/$$i" | sed 's:./$(PROJECT_LOCALE_PATH)\/::g' | sed 's:\/LC_MESSAGES::g'`.utf-8 --no-translator --no-wrap -i $(PROJECT_LOCALE_PATH)/dist/$(LOCALE_GETTEXT_DIR)/$$o.pot -o $$i/$(LOCALE_GETTEXT_DIR)/$$o.po; \
			fi; \
			msguniq $$i/$(LOCALE_GETTEXT_DIR)/$$o.po -o $$i/$(LOCALE_GETTEXT_DIR)/$$o.po; \
		done \
	done

# Generate all .mo files
locale-deploy:
	@echo "----------------"
	@echo "Generate GetText MO files:"
	@list=`$(FIND_LOCALE_SRC)`; \
	for i in $$list;do \
		echo "Compiling  $$i"; \
		msgfmt --statistics $$i -o `echo $$i | sed s/.po$$/.mo/`; \
	done

# Generate all .mo files with fuzzy
locale-deploy-fuzzy:
	@echo "----------------"
	@echo "Generate GetText MO files with Fuzzy translation:"
	@list=`$(FIND_LOCALE_SRC)`; \
	for i in $$list;do \
		echo "Compiling  $$i"; \
		msgfmt -f --statistics $$i -o `echo $$i | sed s/.po/.mo/`; \
	done

# Remove all .mo and .po files
locale-clean:
	@echo "----------------"
	@echo "Clean GetText MO and PO files:"
	@list=`$(FIND_LOCALE_FILES)`; \
	for i in $$list;do \
		echo "Removed $$i"; \
		rm -f $$i; \
	done
	@echo "done"

test:
	@./bin/run-tests.sh
