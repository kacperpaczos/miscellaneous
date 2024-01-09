#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

BASEDIR=$(pwd)
devupdatemenu(){
    clear
    cd $BASEDIR
	echo "Choose option for dev-update: "
	echo "1) Update flatpak packages"
	echo "2) Update apt packages"
    echo "3) Both... "
    echo "*) Any key to exit... "

	read CHOOSE
	case $CHOOSE in
	  1)
	    sudo flatpak update
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        read -p "Remove unused packages [of flatpak]? (y/n): " response

        if [ "$response" == "y" ]; then
            sudo flatpak uninstall --unused
            read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        fi
	    devupdatemenu
	    ;;

	  2)
	    sudo apt update && sudo apt upgrade
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        read -p "Remove unused packages [of apt]? (y/n): " response

        if [ "$response" == "y" ]; then
            sudo apt autoremove
            read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        fi
	    devupdatemenu
	    ;;

      3)
	    sudo flatpak update
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        read -p "Remove unused packages [of flatpak]? (y/n): " response

        if [ "$response" == "y" ]; then
            sudo flatpak uninstall --unused
            read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        fi

        sudo apt update && sudo apt upgrade
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        read -p "Remove unused packages [of apt]? (y/n): " response

        if [ "$response" == "y" ]; then
            sudo apt autoremove
            read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        fi
        devupdatemenu
	    ;;

	  *)
	    mainmenu
	    ;;
	esac
}
devlibmenu (){
    clear
    cd $BASEDIR
	echo "Choose option: "
	echo "1) Install lib*dev: "
	echo "2) Install dev-tools: "
	echo "3) Install dev-tools: "
    echo "*) Any key to exit... "

	read CHOOSE
	case $CHOOSE in
	  1)
	    ;;

	  2)
	    ;;

	  3)
	    ;;

	  *)
	    mainmenu
	    ;;
	esac
}
devtoolsmenu (){

    clear
    cd $BASEDIR
	echo "Choose option for dev-tools: "
	echo "1) Install org.gnome.Builder"
	echo "2) Install git make gcc g++... "
    echo "3) Install Linux Mint devtools... "
    echo "4) Install org.gnome.design.IconLibrary"
    echo "*) Any key to exit... "

	read CHOOSE
	case $CHOOSE in
	  1)
	    sudo flatpak install org.gnome.Builder
	    ;;

	  2)
	    sudo apt install git make gcc g++ meson
	    ;;

      3)
	    sudo apt install mint-dev-tools --install-recommends
	    ;;

      4)
	    sudo flatpak install org.gnome.design.IconLibrary
	    ;;

	  *)
	    mainmenu
	    ;;
	esac
}

xappmenu(){
    clear
    cd $BASEDIR
	echo "Choose option for xapp: "
	echo "1) clone: "
    echo "3) build "
    echo "4) install "
    echo "5) clear ALL "
    echo "*) Any key to exit... "

	read CHOOSE
	case $CHOOSE in
	  1)
        cd xapp-dev
        read -p "Enter the repository URL from which you want to download the program:
        1. https://github.com/kacperpaczos/xapp.git
        2. https://github.com/linuxmint/xapp.git
        Your choice (1/2): " choice

        if [ "$choice" == "1" ]; then
            repo_url="https://github.com/kacperpaczos/xapp.git"
        elif [ "$choice" == "2" ]; then
            repo_url="https://github.com/linuxmint/xapp.git"
        else
            echo "Invalid choice. Please enter the repository URL manually."
            read -p "Repository URL: " repo_url
        fi

        # Clone the repository
        git clone "$repo_url"
        sudo chmod 777 -R ./xapp
        cd xapp
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xappmenu
	    ;;
      2)
        cd xapp
        git fetch upstream
        git checkout master
        git merge upstream/master
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xappmenu
	    ;;
      3)
        sudo apt install libxml2-dev cmake meson libglib2.0-dev libgtk-3-dev libgtksourceview-4-dev libpeas-dev libgnomekbd-dev valac python-gi-dev gir1.2-dbusmenu-gtk3-0.4 libxkbfile-dev libdbusmenu-gtk3-dev
        cd xapp-dev
        cd xapp
        meson --prefix=/usr build
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        ninja -v -C build
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        
	    xappmenu
	    ;;
      4)
        cd xapp-dev
        cd xapp
        sudo ninja install -v -C build
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xappmenu
	    ;;
    
      5)
        
        cd ..
        sudo rm -R ./xapp-dev
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintprojectssmenu
	    ;;
	  *)
	    mintprojectssmenu
	    ;;
	esac

}
mintupdatemenu(){
    clear
    cd $BASEDIR
	echo "Choose option for mintupdate: "
	echo "1) clone: "
    echo "3) build "
    echo "4) install "
    echo "5) clear ALL "
    echo "*) Any key to exit... "

	read CHOOSE
	case $CHOOSE in
	  1)
        mkdir -p mintupdate-dev
        cd mintupdate-dev
        read -p "Enter the repository URL from which you want to download the program (e.g., https://github.com/kacperpaczos/mintupdate.git): " repo_url

        # Clone the repository
        git clone "$repo_url"
        #git clone https://github.com/kacperpaczos/mintupdate.git
        sudo chmod 644 -R ./mintupdate
        cd mintupdate
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintupdatemenu
	    ;;
      2)
        cd ./mintupdate-dev/mintupdate
        pwd
        git fetch upstream
        git checkout master
        git merge upstream/master
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintupdatemenu
	    ;;
      3)
        #sudo apt install libxml2-dev cmake meson libglib2.0-dev libgtk-3-dev libgtksourceview-4-dev libpeas-dev libgnomekbd-dev valac python-gi-dev gir1.2-dbusmenu-gtk3-0.4 libxkbfile-dev
        cd ./mintupdate-dev/mintupdate
        dpkg-buildpackage
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintupdatemenu
	    ;;
      4)
        cd ./mintupdate-dev/
        sudo dpkg -i ./*.deb
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintupdatemenu
	    ;;
    
      5)
        sudo rm -R ./mintupdate-dev
        read -p "Do you want to reinstall the mintupdate package? (yes/no): " answer

        if [[ $answer == "yes" ]]; then
            echo "Removing the mintupdate package..."
            sudo apt purge mintupdate -y
            
            echo "Installing the mintupdate package..."
            sudo apt install mintupdate -y
        fi
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintupdatemenu
	    ;;
	  *)
	    mintprojectssmenu
	    ;;
	esac

}
xedmenu(){
    clear
	echo "Choose option for xed: "
	echo "1) clone: "
    echo "2) syncfork (you need 1 first! ): "
    echo "3) build "
    echo "4) install "
    echo "5) clear ALL "
    echo "*) Any key to exit... "

    cd ..

	read CHOOSE
	case $CHOOSE in
	  1)
        
        cd xed-dev
        git clone https://github.com/kacperpaczos/xed.git
        sudo chmod 777 -R ./xed
        cd xed
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xedmenu
	    ;;
      2)
        cd xed
        git fetch upstream
        git checkout master
        git merge upstream/master
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xedmenu
	    ;;
      3)
        sudo apt install libxml2-dev cmake meson libglib2.0-dev libgtk-3-dev libgtksourceview-4-dev libpeas-dev libgspell-1-dev intltool itstool
        cd xed
        
        meson --prefix=/usr build
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        ninja -v -C build
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xedmenu
	    ;;
      4)
        cd xed
        sudo ninja install -v -C build
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    xedmenu
	    ;;
      5)
        cd ..
        sudo rm -R ./xed-dev
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
	    mintprojectssmenu
	    ;;

	  *)
	    mintprojectssmenu
	    ;;
	esac
}
mintprojectssmenu(){
    clear
    cd $BASEDIR
	echo "Choose option: "
    echo "1) xapp (probably you need this): "
	echo "2) xed: "
    echo "3) mintupdate"
    echo "*) Any key to exit... "
	read CHOOSE
	case $CHOOSE in
	  1)
        mkdir xapp-dev
        sudo chmod 777 -R ./xapp-dev
        cd xapp-dev
	    xappmenu
	    ;;

      2)
        mkdir xed-dev    
        sudo chmod 777 -R ./xed-dev
        cd xed-dev
        
	    xedmenu
	    ;;

      3)mkdir mintupdate-dev
        sudo chmod 777 -R ./mintupdate-dev
        cd mintupdate-dev

        mintupdatemenu
        
        ;;

	  *)
	    mainmenu
	    ;;
	esac
}

mainmenu (){
    clear
    cd $BASEDIR
	echo "Choose option: "
    echo "0) Update the system... "
	echo "1) Install lib*dev: "
	echo "2) Install dev-tools: "
	echo "3) Git, build, install... "
    echo "4) Enable daily builds... "
    echo "5) Install docker on LM... "
    echo "6) Install prompt.sh on LM... "
    echo "7) Install oh-my-bash on LM... "
    echo "*) Any key to exit... "
    
	read CHOOSE
	case $CHOOSE in
      0)
	    devupdatemenu
        mainmenu
	    ;;
	  1)
	    devlibmenu
        mainmenu
	    ;;

	  2)
	    devtoolsmenu
        mainmenu
	    ;;

	  3)
	    mintprojectssmenu
        mainmenu
	    ;;

      4)
	    sudo add-apt-repository ppa:linuxmint-daily-build-team/daily-builds
        sudo apt-get update
        sudo apt-get upgrade
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        mainmenu
	    ;;

      5)
	    sudo apt-get update
        sudo apt-get install ca-certificates curl gnupg
        sudo install -m 0755 -d /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        sudo chmod a+r /etc/apt/keyrings/docker.gpg
        echo \
          "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          "$(. /etc/os-release && echo "jammy")" stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        mainmenu
	    ;;


	  6)
        sudo apt update && sudo apt install wget
        mkdir git-prompt
        cd git-prompt
        wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
        wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
        sudo chmod 664 git-prompt.sh
        sudo chmod 664 git-completion.bash
        cd ..

        echo "Who/where is installing it?"
        original_dir=$(pwd)

        cd /home

        for directory in */; do
            echo " > ${directory%/}"
        done

        cd "$original_dir"

        read -p "Prompt username: " username

        source="./git-prompt"
        destination="/home/$username/.bash_custom"

        echo $source
        echo $destination

        mv "$source" "$destination"

        if [ $? -eq 0 ]; then
          echo "The files has been successfully moved."
          sudo chown -R $username:$username /home/$username/.bash_custom

          echo "$lines_to_add" >> ~/.bashrc
          if [ -f "/home/$username/.bashrc" ]; then
            echo "The .bashrc file exists."
            
            if [ -f "/home/$username/.bashrc_backup" ]; then
                mv "/home/$username/.bashrc_backup" "/home/$username/.bashrc"
                echo "Restored .bashrc_backup to .bashrc."
            fi
            cp "/home/$username/.bashrc" "/home/$username/.bashrc_backup"
            echo "Maked copy /home/$username/.bashrc to /home/$username/.bashrc_backup."

            cp ./bashrc "/home/$username/.bashrc"
          fi

          if [ -f "$HOME/.zshrc" ]; then
            echo "The .zshrc file exists."
            echo "I DO NOTHING!."
          fi

          read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
          mainmenu
        else
          echo "An error occurred while moving the files."
          sudo rm -Rf ./git-prompt
          read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
          mainmenu
        fi

        ;;

      7)
        sudo apt update && sudo apt install wget
        mkdir ohmybash
        cd ohmybash
	    bash -c "$(wget https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh -O -)"
        cd ..
        read -p "...ENDED! PRESS ANY KEY TO ESCAPE!"
        mainmenu
	    ;;


      *)
	    exit
	    ;;
	esac
}

mainmenu
