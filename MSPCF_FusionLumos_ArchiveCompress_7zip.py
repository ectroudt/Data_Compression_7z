import os
import subprocess


def run_7z_command(arc_filename, data_dir, exec_7z="C:/Program Files/7-Zip/7z.exe"):
    
    
    result = subprocess.run([exec_7z, "a", "-t7z", arc_filename, data_dir], capture_output=True, text=True)
    
    if result.stderr:
        
        raise subprocess.CalledProcessError(returncode=result.returncode,
                                            cmd=result.args,
                                            stderr=result.stderr)
    if result.stdout:
        
        print(result.stdout)


def get_folder_size_GB(filepath):

    totalsize = os.path.getsize(filepath) 

    for item in os.listdir(filepath):

        cur_path = os.path.join(filepath, item)

        if (os.path.isfile(cur_path)) and not (os.path.islink(cur_path)):

            totalsize += (os.path.getsize(cur_path) / (10**9))

        elif os.path.isdir(cur_path):

            totalsize += get_folder_size_GB(cur_path)

        else:
            pass

    return totalsize

        
def compress_dir(cur_dir, dest_dir, track):        
    
    track += 1

    cur_data_dir = cur_dir
    dest_dir = dest_dir
    
    failed = []
    
    for ms_data in os.listdir(cur_data_dir):

        active_dir = os.path.join(cur_data_dir, ms_data)
        active_dir = active_dir.replace("\\", "/")
        
        if os.path.isfile(active_dir):
            arc_data_dest = str(os.path.join(dest_dir, ms_data, ".7z"))
            arc_data_dest = arc_data_dest.replace("\\", "/")

            if "/.7z" in arc_data_dest:

                arc_data_dest = arc_data_dest.replace("/.7z", ".7z")
        
            print("-" * 95)
            print("\n\n Passing " + str(active_dir) + " as argument to 7zip..\n\n")
            print("\n\nCreating archive of data at: " + arc_data_dest + "\n\n")

        
                
            try:
                
                run_7z_command(arc_filename=arc_data_dest, data_dir=active_dir)
            
            except subprocess.CalledProcessError as runerror:
                
                print("Error encountered: " + str(runerror.stderr.decode("utf-8")))
                failed.append(ms_data)

            except:

                print("Unidentified error encountered..\n\n")
                failed.append(ms_data)

            print("-" * 95)

        else:

            folder_size = get_folder_size_GB(active_dir)

            if (folder_size <= 31) and (track > 1):
            
                arc_data_dest = str(os.path.join(dest_dir, ms_data, ".7z"))    
                arc_data_dest = arc_data_dest.replace("\\", "/")

                if "/.7z" in arc_data_dest:

                    arc_data_dest = arc_data_dest.replace("/.7z", ".7z")
        
                print("-" * 95)
                print("\n\n Passing " + str(active_dir) + " as argument to 7zip..\n\n")
                print("\n\nCreating archive of data at: " + arc_data_dest + "\n\n")
                       
                try:
                                
                  run_7z_command(arc_filename=arc_data_dest, data_dir=active_dir)
                            
                except subprocess.CalledProcessError as runerror:
                                
                  print("Error encountered: " + str(runerror.stderr.decode("utf-8")))
                  failed.append(ms_data)

                except:

                  print("Unidentified error encountered..\n\n")
                  failed.append(ms_data)

                print("-" * 95)

            elif folder_size > 31:

                if (ms_data != "Sciex_MS_BackUps") and (ms_data != "WindowsImageBackup"):

                    new_dest_dir = str(os.path.join(dest_dir, ms_data))
                    new_dest_dir = new_dest_dir.replace("\\", "/")
    
                    print("\n\n---->  creating new destination directory at: " + new_dest_dir + "\n\n")
                    os.mkdir(new_dest_dir)
                    
                    if track == 1:

                        failed.append(ms_data)


                    
                    compress_dir(active_dir, new_dest_dir, track)
            else:
                pass
    

    if len(failed) > 0:
        
        with open("Error_log", "w") as elog:

            for msdir in failed:
            
                elog.write(str(msdir) + "\n")
    


def main():

    FDrive_dir = "F:/Fusion_back-up/"
    Backup_dir="E:/Compressed_FL_Backups/ALL_Previous_Data_to_Aug2020/"

    start_track = 0
    
    compress_dir(FDrive_dir, Backup_dir, start_track)
        

main()
         
